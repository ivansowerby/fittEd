import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations

# Read your CSV file
df = pd.read_csv("./data.csv")

# Select only numeric columns (so plots make sense)
numeric_df = df.select_dtypes(include=['number'])

# Generate all unique pairs of columns
def yep():
    for col1, col2 in combinations(numeric_df.columns, 2):
        plt.figure()
        plt.scatter(numeric_df[col1], numeric_df[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title(f"{col1} vs {col2}")
        # plt.show()
        open(f"{col1}_vs_{col2}.png", "w").close()
        plt.savefig(f"./fig/{col1}_vs_{col2}")

x = "n_tx"
y = "size"

plt.figure()
plt.scatter(numeric_df[x], numeric_df[y])
plt.xlabel(x)
plt.ylabel(y)
plt.xscale("function", functions=(lambda t: t, lambda t: t))
# plt.xscale("logit")
# plt.yscale("log")
plt.title("idk")
plt.show()