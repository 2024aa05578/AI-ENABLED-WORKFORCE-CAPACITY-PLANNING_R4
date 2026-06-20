import pandas as pd
import math


def calculate_workforce(
    df,
    bau_growth,
    dc_growth,
    attrition
):

    annual_capacity = 1680

    result = []

    for _, row in df.iterrows():

        current_hours = (
            row["Breakdown_WO"] * row["Breakdown_Hrs"]
            + row["PM_WO"] * row["PM_Hrs"]
            + row["Startup_WO"] * row["Startup_Hrs"]
        )

        future_hours = current_hours * (
            1
            + (bau_growth / 100)
            + (dc_growth / 100)
        )

        required_engineers = (
            future_hours /
            annual_capacity
        )

        available_engineers = (
            row["Current_SE"]
            * (1 - attrition / 100)
        )

        hiring_required = max(
            math.ceil(
                required_engineers
                - available_engineers
            ),
            0
        )

        result.append(
            {
                "Region": row["Region"],
                "Product": row["Product"],
                "Current Hours": round(current_hours),
                "Future Hours": round(future_hours),
                "Required Engineers": round(
                    required_engineers, 1
                ),
                "Available Engineers": round(
                    available_engineers, 1
                ),
                "Additional Required": hiring_required
            }
        )

    return pd.DataFrame(result)
