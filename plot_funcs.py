from plot_vars import AXIS_WIDTH, TICK_PARAMS_WIDTH, FONT_BIG


def paint_it_black(axes):
    for ax in axes.flat:
        # Painting the spines in black
        for spine in ax.spines.values():
            spine.set_color("black")
            spine.set_linewidth(AXIS_WIDTH)
            # Painting the ticks in black
        ax.tick_params(colors="black", width=TICK_PARAMS_WIDTH)
        # Painting the tick labels in black\n",
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_color("black")
        # Painting the axis labels in black\n",
        ax.xaxis.label.set_color("black")
        ax.yaxis.label.set_color("black")


def add_plot_labels(ax, label):
    ax.text(
        0.1, 0.9, label, transform=ax.transAxes, fontweight="bold", va="top", ha="right", fontsize=FONT_BIG
    )


# Unused code to plot sigmas

# Sigma
# Horizontal dashed lines
""""
y11, y12 = 0.135, 0.17
y21, y22 = 0.115, 0.18
left_one_sigma = 0.07
left_two_sigma = 0.045
left_axis = 0.1
left_end = 0.12
dark_gray = '#8c8c8c'
light_gray = '#d9d9d9'

# Horizontal dashed lines for one sigma
fig.add_artist(Line2D([left_one_sigma, left_end], [y11, y11], color=dark_gray, linestyle='--', linewidth=1, transform=fig.transFigure))
fig.add_artist(Line2D([left_one_sigma, left_end], [y12, y12], color=dark_gray, linestyle='--', linewidth=1, transform=fig.transFigure))

# Horizontal dashed lines for two sigma
fig.add_artist(Line2D([left_two_sigma, left_axis - 0.01], [y21, y21], color=light_gray, linestyle='--', linewidth=1, transform=fig.transFigure))
fig.add_artist(Line2D([left_two_sigma,  left_axis - 0.01], [y22, y22], color=light_gray, linestyle='--', linewidth=1, transform=fig.transFigure))
fig.add_artist(Line2D([left_axis, left_end], [y21, y21], color=light_gray, linestyle='--', linewidth=1, transform=fig.transFigure))
fig.add_artist(Line2D([left_axis, left_end], [y22, y22], color=light_gray, linestyle='--', linewidth=1, transform=fig.transFigure))

# Vertical line with arrows for one sigma
fig.add_artist(FancyArrowPatch((left_one_sigma, y11), (left_one_sigma, y12), arrowstyle='<->', color=dark_gray, transform=fig.transFigure))

# Vertical line with arrows for two sigma
fig.add_artist(FancyArrowPatch((left_two_sigma, y21), (left_two_sigma, y22), arrowstyle='<->', color=light_gray, transform=fig.transFigure))

# Vertical sigma label for one and two sigma
fig.text(left_one_sigma - 0.015, (y11 + y12) / 2, r'$\sigma$', verticalalignment='center', fontsize=20, color=dark_gray, rotation='vertical', transform=fig.transFigure)
fig.text(left_two_sigma - 0.015, (y21 + y22) / 2, r'$2 \sigma$', verticalalignment='center', fontsize=20, color=light_gray, rotation='vertical', transform=fig.transFigure)
"""
