import pandas as pd
import math

PRODUCTIVE_HOURS_PER_DAY = 7
WORKING_DAYS_PER_MONTH = 20
MONTHS_PER_YEAR = 12

ANNUAL_CAPACITY = (
    PRODUCTIVE_HOURS_PER_DAY
    * WORKING_DAYS_PER_MONTH
    * MONTHS_PER_YEAR
)


def calculate_workforce(
        df,
        bau_growth,
        dc_growth,
        attrition):

    results = []

    for _, row in df.iterrows():

        # Current Workload

        current_hours = (
            row["Breakdown_WO"] * row["Breakdown_Hrs"]
            + row["PM_WO"] * row["PM_Hrs"]
            + row["Startup_WO"] * row["Startup_Hrs"]
        )

        # Future workload

        growth_factor = (
            1
            + (bau_growth / 100)
            + (dc_growth / 100)
        )

        future_hours = (
            current_hours * growth_factor
        )

        # Engineers required

        required_engineers = (
            future_hours /
            ANNUAL_CAPACITY
        )

        # Attrition adjustment

        available_engineers = (
            row["Current_SE"]
            * (1 - attrition / 100)
        )

        # Hiring Gap

        additional_required = max(
            math.ceil(
                required_engineers
                - available_engineers
            ),
            0
        )

        results.append({

            "Region":
                row["Region"],

            "Product":
                row["Product"],

            "Current Hours":
                round(current_hours),

            "Future Hours":
                round(future_hours),

            "Required Engineers":
                round(required_engineers, 1),

            "Available Engineers":
                round(available_engineers, 1),

            "Additional Required":
                additional_required

        })

    return pd.DataFrame(results)
