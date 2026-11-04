from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "datasets" / "creditcard.csv"

df = pd.read_csv(DATASET_PATH)

print("=" * 80)
print("Dataset Information")
print("=" * 80)

print(df.info())

print("\n")

print(df.describe())

print("\nMissing Values")

print(df.isnull().sum())

fraud_counts = df["Class"].value_counts()

print(fraud_counts)

fraud_counts.plot(kind="bar")

plt.title("Fraud vs Normal Transactions")

plt.xlabel("Class")

plt.ylabel("Count")

plt.show()

plt.figure(figsize=(10,5))

plt.hist(df["Amount"], bins=100)

plt.title("Transaction Amount Distribution")

plt.xlabel("Amount")

plt.ylabel("Frequency")

plt.show()

fraud = df[df["Class"] == 1]

normal = df[df["Class"] == 0]

print("Fraud Mean Amount")

print(fraud["Amount"].mean())

print("Normal Mean Amount")

print(normal["Amount"].mean())

plt.figure(figsize=(12,4))

plt.hist(df["Time"], bins=100)

plt.title("Transaction Time")

plt.show()

corr = df.corr()

plt.figure(figsize=(15,15))

plt.imshow(corr)

plt.colorbar()

plt.title("Correlation Matrix")

plt.show()

fraud_percent = (df["Class"].sum()/len(df))*100

print(f"Fraud Percentage : {fraud_percent:.4f}%")