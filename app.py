import concurrent.futures
import csv
import datetime
import os
import time


def fetch_google_api_data(date):
    # Method already implemented as mention in the description
    pass

def get_data_specific_to_date(date):
    try:
        data = fetch_google_api_data(date)
        return date, data
    except Exception as e:
        print(f"Error fetching data for {date}: {e}")
        return date, None

def date_range(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    diff = end_date - start_date
    return [(start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(diff.days + 1)]

def main(start_date, end_date, output_folder):
    dates = date_range(start_date, end_date)
    final_data = {}

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_date = {executor.submit(get_data_specific_to_date, date): date for date in dates}
        for future in concurrent.futures.as_completed(future_to_date):
            date = future_to_date[future]
            try:
                date, data = future.result()
                if data is not None:
                    final_data[date] = data
            except Exception as e:
                print(f"Exception occurred: {e}")

    save_data_to_csv(final_data, output_folder)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

def save_data_to_csv(data, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, 'final_data.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Data'])
        for date, content in data.items():
            writer.writerow([date, content])

if __name__ == "__main__":
    start_date = '2023-01-01'
    end_date = '2023-02-10'
    output_folder = './data'

    main(start_date, end_date, output_folder)