import pandas as pd
import json
from ydata_profiling import ProfileReport

def generate_eda_report(data_path, output_report_path, output_insights_path):
    """
    Generate EDA report and save insights to a JSON file.

    Parameters:
        data_path (str): Path to the input dataset.
        output_report_path (str): Path to save the HTML report.
        output_insights_path (str): Path to save the JSON insights.

    Returns:
        dict: Key insights extracted from the dataset.
    """
    # Load dataset
    data = pd.read_csv(data_path)
    
    # Generate HTML report
    profile = ProfileReport(data, title="EDA Report", explorative=True)
    profile.to_file(output_report_path)

    # Extract key insights
    insights = {
        "shape": {"rows": data.shape[0], "columns": data.shape[1]},
        "missing_values": data.isnull().sum().to_dict(),
        "summary_stats": data.describe().to_dict(),
        "columns": list(data.columns),
    }

    # Save insights to JSON
    with open(output_insights_path, "w") as file:
        json.dump(insights, file, indent=4)
    
    print(f"EDA report saved to {output_report_path}")
    print(f"EDA insights saved to {output_insights_path}")
    return insights


