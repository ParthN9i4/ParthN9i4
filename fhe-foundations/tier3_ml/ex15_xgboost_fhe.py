"""Exercise 15 -- Concrete-ML Encrypted XGBoost

Concrete-ML wraps familiar scikit-learn-style estimators and compiles them
into FHE circuits.  Under the hood it:
  1. Trains a normal model (XGBoost, logistic regression, neural net, ...).
  2. Quantizes the model weights and decision thresholds to `n_bits` bits.
  3. Compiles the quantized model into a TFHE *integer* circuit -- encrypted
     integer arithmetic plus programmable-bootstrapping table lookups, not a
     gate-level boolean circuit.
  4. Runs inference entirely on encrypted data.

The key trade-off is **quantization bitwidth**:
  * Fewer bits  -> faster FHE evaluation, but lower accuracy.
  * More bits   -> higher accuracy, but slower (deeper) circuit.

This exercise trains an XGBoost classifier on a synthetic 2D dataset
(make_moons) and compares plain-sklearn accuracy vs Concrete-ML accuracy
at different quantization levels.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from sklearn.datasets import make_moons
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from xgboost import XGBClassifier as SklearnXGB
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    from concrete.ml.sklearn import XGBClassifier as ConcreteXGB
    HAS_CONCRETE = True
except ImportError:
    HAS_CONCRETE = False


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------

def make_dataset(n_samples=300, noise=0.25, random_state=42):
    """Create a synthetic 2D binary classification dataset (two moons).

    Returns
    -------
    X_train, X_test, y_train, y_test : arrays
    """
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=random_state)
    return train_test_split(X, y, test_size=0.3, random_state=random_state)


def train_plain_xgboost(X_train, y_train):
    """Train a standard scikit-learn / XGBoost classifier.

    Returns
    -------
    model : XGBClassifier
        Fitted sklearn XGBoost model.
    """
    model = SklearnXGB(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def train_concrete_xgboost(X_train, y_train, n_bits=6):
    """Train a Concrete-ML XGBoost classifier with quantization.

    Parameters
    ----------
    X_train, y_train : arrays
        Training data.
    n_bits : int
        Quantization bitwidth (fewer bits = faster FHE, lower accuracy).

    Returns
    -------
    model : ConcreteXGB
        Fitted Concrete-ML XGBoost model (ready for FHE compilation).
    """
    model = ConcreteXGB(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        n_bits=n_bits,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def compare_accuracy(plain_model, concrete_model, X_test, y_test):
    """Compare plain vs quantized-Concrete accuracy on the test set.

    The `fhe` argument of Concrete-ML's predict() selects the execution mode
    and DEFAULTS TO "disable" -- i.e. plain predict() runs the quantized
    model in the clear and involves no FHE circuit at all.  The three modes:

        fhe="disable"   (default) quantized inference in the clear
        fhe="simulate"  emulates the FHE circuit, including its noise, in
                        the clear -- the right choice for accuracy studies
        fhe="execute"   real FHE execution (correct, but orders of
                        magnitude slower)

    We use "simulate" here: it reflects what the FHE circuit would actually
    produce without paying the cost of real encrypted execution.  Note that
    predict(fhe="simulate"/"execute") requires the model to be compiled
    first.

    Returns
    -------
    plain_acc, concrete_acc : float
        Accuracy of each model.
    """
    plain_preds = plain_model.predict(X_test)
    plain_acc = accuracy_score(y_test, plain_preds)

    # Explicitly request simulation; the default would silently skip FHE.
    concrete_preds = concrete_model.predict(X_test, fhe="simulate")
    concrete_acc = accuracy_score(y_test, concrete_preds)

    return plain_acc, concrete_acc


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
print("=== ex15: Concrete-ML Encrypted XGBoost ===\n")

if not HAS_SKLEARN:
    print("  sklearn / xgboost not installed -- skipping all tests.")
    print("  Install with: pip install scikit-learn xgboost\n")

if HAS_SKLEARN:
    X_train, X_test, y_train, y_test = make_dataset()

    # --- Plain XGBoost ---
    plain_model = train_plain_xgboost(X_train, y_train)
    plain_acc = accuracy_score(y_test, plain_model.predict(X_test))
    print(f"  Plain XGBoost accuracy:  {plain_acc:.3f}")
    check("plain XGBoost accuracy > 0.80", plain_acc > 0.80)

    if HAS_CONCRETE:
        # --- Concrete-ML at 6 bits ---
        concrete_6 = train_concrete_xgboost(X_train, y_train, n_bits=6)
        plain_acc_6, conc_acc_6 = compare_accuracy(plain_model, concrete_6, X_test, y_test)
        print(f"  Concrete-ML (6-bit) accuracy: {conc_acc_6:.3f}")
        check("6-bit Concrete accuracy > 0.75", conc_acc_6 > 0.75)

        # --- Concrete-ML at 2 bits ---
        concrete_2 = train_concrete_xgboost(X_train, y_train, n_bits=2)
        plain_acc_2, conc_acc_2 = compare_accuracy(plain_model, concrete_2, X_test, y_test)
        print(f"  Concrete-ML (2-bit) accuracy: {conc_acc_2:.3f}")

        # --- Quantization trade-off ---
        print(f"\n  Accuracy comparison:")
        print(f"    Plain XGBoost:    {plain_acc:.3f}")
        print(f"    Concrete 6-bit:   {conc_acc_6:.3f}")
        print(f"    Concrete 2-bit:   {conc_acc_2:.3f}")
        check("6-bit >= 2-bit accuracy (quantization trade-off)",
              conc_acc_6 >= conc_acc_2)
        check("plain >= 6-bit accuracy (quantization costs accuracy)",
              plain_acc >= conc_acc_6 - 0.05)  # small tolerance
    else:
        print("\n  Concrete-ML not installed -- skipping FHE tests.")
        print("  Install with: pip install concrete-ml")
        print("\n  What would happen:")
        print("  - A Concrete-ML XGBClassifier would be trained at 6-bit and 2-bit")
        print("    quantization levels.")
        print("  - The 6-bit model would achieve accuracy close to plain XGBoost")
        print("    (typically within 2-5%).")
        print("  - The 2-bit model would lose more accuracy due to aggressive")
        print("    quantization, but would evaluate faster as an FHE circuit.")
        print("  - The model could then be compiled with model.compile(X_train)")
        print("    and run on encrypted inputs with model.predict(X_test, fhe='execute').")

summary()
