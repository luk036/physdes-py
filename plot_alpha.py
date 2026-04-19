import matplotlib.pyplot as plt

from physdes.router.global_router import GlobalRouter


def main() -> None:
    from tests.conftest import generate_random_points

    source, terminals = generate_random_points()

    alphas = [1.0 + i * 0.02 for i in range(20)]
    wirelengths = []

    for alpha in alphas:
        router = GlobalRouter(source, terminals)
        router.route_with_constraints(alpha)
        wirelength = router.tree.calculate_total_wirelength()
        wirelengths.append(wirelength)

    plt.figure(figsize=(10, 6))
    plt.plot(alphas, wirelengths, marker="o", linewidth=2, markersize=8)
    plt.xlabel("Alpha", fontsize=12)
    plt.ylabel("Total Wirelength", fontsize=12)
    plt.title("Total Wirelength vs Alpha Parameter", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(alphas)

    plt.tight_layout()
    plt.savefig("wirelength_vs_alpha_small.png", dpi=150)


if __name__ == "__main__":
    main()
