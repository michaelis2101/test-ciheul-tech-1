import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import DatetimeTickFormatter

def parse_bandwidth_data(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        timestamp = None
        for line in lines:
            if "Timestamp" in line:
                timestamp = line.split("Timestamp:")[1].strip()
            elif "sec" in line and "Mbits/sec" in line:
                try:
                    bitrate = float(line.split()[6])
                    data.append((timestamp, bitrate))
                except ValueError:
                    continue
    df = pd.DataFrame(data, columns=["Timestamp", "Bitrate"])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    df = df.groupby('Timestamp', as_index=False).mean()
    
    return df

df = parse_bandwidth_data("soal_chart_bokeh.txt")


output_file("bandwidth_chart.html")


p = figure(title="Testing Jaringan", 
           x_axis_type='datetime', 
           width=800, height=400)

# Plot line
p.line(df['Timestamp'], df['Bitrate'], line_width=2)

# Customize axis labels
p.xaxis.axis_label = 'DATE TIME'
p.yaxis.axis_label = 'Speed (Mbps)'

# Set Y-axis range
p.y_range.start = 0
p.y_range.end = 125  # Set it to go up to 125 Mbps

# Correct the X-axis datetime tick format
p.xaxis.major_label_orientation = 3.14 / 4  # Rotate x-axis labels

# Correct the X-axis datetime tick format
p.xaxis.major_label_orientation = 3.14 / 4  # Rotate x-axis labels
p.xaxis.formatter = DatetimeTickFormatter(
    hours="%m/%d/%Y %H:%M",
    days="%m/%d/%Y",
    months="%m/%d/%Y",
    years="%m/%d/%Y"
)

show(p)
