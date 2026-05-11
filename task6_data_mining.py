import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlxtend.frequent_patterns import apriori, association_rules

print("=== TASK 6: DATA WAREHOUSING & MINING ===")

# --- 1. Star Schema & Sample Data Generation ---
# Fact Table: Sales
# Dimension Tables: Customer, Product
data = {
    'sale_id': [1, 2, 3, 4, 5, 6, 7],
    'cust_age': [25, 34, 22, 45, 52, 23, 40],
    'cust_income': [50000, 60000, 30000, 80000, 100000, 20000, 75000],
    'bought_laptop': [1, 1, 0, 1, 1, 0, 1],
    'bought_mouse': [1, 0, 1, 1, 0, 1, 1],
    'bought_keyboard': [0, 1, 0, 1, 0, 0, 1]
}
df = pd.DataFrame(data)
print("\n--- Sales Fact Table Sample (Star Schema representation) ---")
print(df.head(3))

# --- 2. Classification (Predict if customer buys a laptop) ---
X = df[['cust_age', 'cust_income']]
y = df['bought_laptop']

# Train-test split & Decision Tree
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf = DecisionTreeClassifier(max_depth=2).fit(X_train, y_train)
preds = clf.predict(X_test)

print("\n--- Classification ---")
print(f"Accuracy predicting 'bought_laptop' based on age/income: {accuracy_score(y_test, preds)*100:.2f}%")

# --- 3. Association Rule Mining ---
print("\n--- Association Rule Mining ---")
basket = df[['bought_laptop', 'bought_mouse', 'bought_keyboard']].astype(bool)

# Find frequent itemsets (support >= 0.3)
frequent_itemsets = apriori(basket, min_support=0.3, use_colnames=True)
print("Frequent Itemsets:")
print(frequent_itemsets)

# Generate rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5, num_itemsets=len(frequent_itemsets))
print("\nAssociation Rules (If A -> Then B):")
print(rules[['antecedents', 'consequents', 'support', 'confidence']])
