#################################################################################
# WaterTAP Copyright (c) 2020-2026, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory, Oak Ridge National Laboratory,
# National Laboratory of the Rockies, and National Energy Technology
# Laboratory (subject to receipt of any required approvals from the U.S. Dept.
# of Energy). All rights reserved.
#
# Please see the files COPYRIGHT.md and LICENSE.md for full copyright and license
# information, respectively. These files are also available online at the URL
# "https://github.com/watertap-org/watertap/"
#################################################################################

__author__ = "Marcus Holly"

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
from scipy.interpolate import LinearNDInterpolator

FEED, REC = "# Feed Concentration", "Volumetric Recovery Rate"

# What the user can color the map by: {dropdown label: column in the sweep results}
METRICS = {
    "LCOW ($/m³)": "LCOW",
    "Specific energy consumption (kWh/m³)": "SEC",
    "Total membrane area (m²)": "Total Membrane Area",
    "Final brine concentration (g/L)": "Final Brine Concentration",
}

# Components of LCOW, shown as a stacked bar for the selected operating point
LCOW_PARTS = {
    "Primary pumps": "Primary Pump Capex LCOW",
    "Booster pumps": "Booster Pump Capex LCOW",
    "ERD": "ERD Capex LCOW",
    "Membranes": "Membrane Capex LCOW",
    "Indirect capex": "Indirect Capex LCOW",
    "Electricity": "Electricity LCOW",
    "Membrane replacement": "Membrane Replacement LCOW",
    "Chem/labor/maint.": "Chem-labor-maintenance LCOW",
}


def launch_lsrro_explorer(results):
    """Interactive explorer for the sweep results returned by feed_concentration_recovery_profile."""
    feeds = np.sort(results[FEED].unique())
    recs = np.sort(results[REC].unique())

    def scale(rec, feed):
        """Normalize (recovery, feed) to the unit square so triangles are well shaped."""
        rec, feed = np.atleast_1d(rec), np.atleast_1d(feed)
        return np.column_stack(
            [
                (rec - recs.min()) / np.ptp(recs),
                (feed - feeds.min()) / np.ptp(feeds),
            ]
        )

    def interpolator(col):
        # Interpolate over solved points only; outside their hull the result is NaN ("no solution")
        ok = results[col].notna()
        return LinearNDInterpolator(
            scale(results.loc[ok, REC], results.loc[ok, FEED]),
            results.loc[ok, col].to_numpy(),
        )

    interps = {c: interpolator(c) for c in [*METRICS.values(), *LCOW_PARTS.values()]}
    fx = np.linspace(feeds.min(), feeds.max(), 60)
    fy = np.linspace(recs.min(), recs.max(), 60)
    R, F = np.meshgrid(fy, fx, indexing="ij")

    def at(col, feed, rec):
        return float(interps[col](scale(rec, feed))[0])

    def draw(metric_label, feed, rec):
        col = METRICS[metric_label]
        fig, (ax_map, ax_bar) = plt.subplots(
            1, 2, figsize=(11, 4.3), gridspec_kw={"width_ratios": [1.6, 1]}
        )

        # Left: map of the selected metric over the swept design space
        Z = np.ma.masked_invalid(
            interps[col](scale(R.ravel(), F.ravel())).reshape(R.shape)
        )
        if Z.mask.all():
            ax_map.text(
                0.5,
                0.5,
                "No solved points in sweep",
                ha="center",
                transform=ax_map.transAxes,
            )
        else:
            cf = ax_map.contourf(fx, fy, Z, levels=12, cmap="viridis")
            fig.colorbar(cf, ax=ax_map, label=metric_label)
        ax_map.plot(feed, rec, marker="*", ms=18, mfc="white", mec="black", ls="none")
        ax_map.set(
            xlabel="Feed concentration (g/L)", ylabel="Overall water recovery (-)"
        )
        ax_map.set_title("Design space (grey = outside solved region)", fontsize=11)
        ax_map.set_facecolor("0.85")

        # Right: LCOW breakdown at the selected point
        parts = {k: at(c, feed, rec) for k, c in LCOW_PARTS.items()}
        if any(np.isnan(v) for v in parts.values()):
            ax_bar.text(
                0.5,
                0.5,
                "Outside the solved region\n(sweep point infeasible\nor not converged)",
                ha="center",
                va="center",
                transform=ax_bar.transAxes,
            )
            ax_bar.axis("off")
            fig.suptitle(
                f"Feed {feed:.0f} g/L, recovery {rec:.0%}: no solution in sweep",
                fontweight="bold",
            )
        else:
            bottom = 0.0
            for (name, v), color in zip(
                parts.items(), plt.cm.Set2(np.linspace(0, 1, len(parts)))
            ):
                ax_bar.bar(0, v, bottom=bottom, color=color, width=0.5, label=name)
                bottom += v
            ax_bar.set(xlim=(-0.6, 0.6), xticks=[], ylabel="LCOW ($/m³)")
            ax_bar.set_title("Cost breakdown at the ★", fontsize=11)
            ax_bar.legend(
                loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=9
            )
            ax_bar.spines[["top", "right"]].set_visible(False)
            fig.suptitle(
                f"Feed {feed:.0f} g/L, recovery {rec:.0%}  →  "
                f"LCOW ${at('LCOW', feed, rec):.2f}/m³  |  "
                f"SEC {at('SEC', feed, rec):.1f} kWh/m³  |  "
                f"membrane area {at('Total Membrane Area', feed, rec):,.0f} m²",
                fontweight="bold",
            )
        fig.tight_layout()
        return fig

    def show(metric_label, feed, rec):
        draw(metric_label, feed, rec)
        plt.show()

    w_metric = widgets.Dropdown(
        options=list(METRICS),
        description="Map shows:",
        style={"description_width": "initial"},
    )
    w_feed = widgets.FloatSlider(
        value=float(feeds.min()),
        min=float(feeds.min()),
        max=float(feeds.max()),
        step=1,
        description="Feed (g/L):",
        continuous_update=False,
        layout=widgets.Layout(width="360px"),
    )
    w_rec = widgets.FloatSlider(
        value=float(recs.min()),
        min=float(recs.min()),
        max=float(recs.max()),
        step=0.01,
        readout_format=".0%",
        description="Recovery:",
        continuous_update=False,
        layout=widgets.Layout(width="360px"),
    )
    out = widgets.interactive_output(
        show, {"metric_label": w_metric, "feed": w_feed, "rec": w_rec}
    )
    display(widgets.VBox([widgets.HBox([w_metric, w_feed, w_rec]), out]))
    return draw  # handy for testing / saving figures
