
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

# ==========================================
# CONFIGURATION
# ==========================================

# Reproducible synthetic datasets
random.seed(42)

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def random_date(start, max_days):
    return start + timedelta(days=random.randint(0, max_days))


def generate_mock_ic(customer_no, dob):
    """
    Deliberately fictional identifier.
    Not a valid Malaysian identification number.
    """
    return f"MOCK-IC-{customer_no:04d}-{dob.year}"


def generate_mock_phone(customer_no):
    """
    Deliberately fictional phone number.
    Not a real Malaysian phone number.
    """
    return f"MOCK-PHONE-{customer_no:04d}"


def save_csv(filename, headers, rows):
    filepath = DATA_DIR / filename

    with filepath.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Saved: {filename} ({len(rows)} rows)")


# ==========================================
# 1. GENERATE CUSTOMER DATA
# ==========================================

def generate_customers():
    customers = []
    customer_ids = []

    first_names = [
        "Alex", "Jordan", "Taylor", "Morgan",
        "Casey", "Riley", "Jamie", "Avery"
    ]

    last_names = [
        "Example", "Sample", "Demo", "Test"
    ]

    for i in range(1, 101):
        customer_id = f"CUST{1000 + i}"
        customer_ids.append(customer_id)

        gender_raw = random.choice([
            "M", "F", "Male", "Female", "m", "f"
        ])

        dob = random_date(datetime(1970, 1, 1), 11000)

        dob_str = dob.strftime(
            random.choice([
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%d-%m-%Y",
                "%Y/%m/%d",
            ])
        )

        name = (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        )

        # Intentional missing identification values
        ic_no = (
            generate_mock_ic(i, dob)
            if random.random() > 0.05
            else ""
        )

        # Intentional invalid phone values
        if random.random() < 0.08:
            phone = "INVALID_PHONE"
        else:
            phone = generate_mock_phone(i)

        created_at = random_date(
            datetime(2015, 1, 1), 3000
        ).strftime("%Y-%m-%d")

        customers.append([
            customer_id,
            name,
            ic_no,
            phone,
            dob_str,
            gender_raw,
            created_at,
        ])

    # Intentional duplicate rows
    for _ in range(5):
        customers.append(
            random.choice(customers[:100]).copy()
        )

    save_csv(
        "customer_master.csv",
        [
            "cust_id",
            "full_name",
            "ic_no",
            "phone_no",
            "dob",
            "gender",
            "created_at",
        ],
        customers,
    )

    return customer_ids


# ==========================================
# 2. GENERATE ACCOUNT DATA
# ==========================================

def generate_accounts(customer_ids):
    accounts = []
    account_ids = []

    account_types = [
        "Savings",
        "Current",
        "SAVINGS_ACC",
        "CURRENT_ACC",
        "INVALID_TYPE",
        "Fixed Deposit",
    ]

    statuses = [
        "Active", "Dormant", "ACTIVE", "CLOSED", "A"
    ]

    for i in range(1, 151):
        account_id = f"ACC{5000 + i}"
        account_ids.append(account_id)

        # Intentional orphan records
        if i > 140:
            customer_id = f"CUST999{i}"
        else:
            customer_id = random.choice(customer_ids)

        account_type = random.choice(account_types)

        balance = round(
            random.uniform(50, 75000), 2
        )

        # Intentional negative balances
        if random.random() < 0.05:
            balance = -balance

        status = random.choice(statuses)

        opened_date = random_date(
            datetime(2018, 1, 1), 2000
        ).strftime("%Y-%m-%d")

        accounts.append([
            account_id,
            customer_id,
            account_type,
            balance,
            status,
            opened_date,
        ])

    save_csv(
        "account_master.csv",
        [
            "account_id",
            "cust_id",
            "account_type",
            "balance",
            "status",
            "opened_date",
        ],
        accounts,
    )

    return account_ids


# ==========================================
# 3. GENERATE TRANSACTION DATA
# ==========================================

def generate_transactions(account_ids):
    transactions = []

    transaction_types = [
        "DEPOSIT",
        "WITHDRAWAL",
        "TRANSFER",
        "DEP",
        "WD",
        "INVALID_TXN",
    ]

    for i in range(1, 1001):
        transaction_id = f"TXN{100000 + i}"

        # Intentional orphan transactions
        if i > 970:
            account_id = f"ACC888{i}"
        else:
            account_id = random.choice(account_ids)

        transaction_type = random.choice(
            transaction_types
        )

        amount = round(
            random.uniform(10, 5000), 2
        )

        transaction_date = random_date(
            datetime(2023, 1, 1), 365
        ).strftime(
            random.choice([
                "%Y-%m-%d %H:%M:%S",
                "%d/%m/%Y %H:%M",
            ])
        )

        transactions.append([
            transaction_id,
            account_id,
            transaction_type,
            amount,
            transaction_date,
        ])

    save_csv(
        "transaction_history.csv",
        [
            "transaction_id",
            "account_id",
            "txn_type",
            "amount",
            "txn_date",
        ],
        transactions,
    )


# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    print("Generating synthetic banking datasets...\n")

    customer_ids = generate_customers()
    account_ids = generate_accounts(customer_ids)
    generate_transactions(account_ids)

    print("\nAll synthetic datasets generated!")
    print(f"Output folder: {DATA_DIR}")


if __name__ == "__main__":
    main()
