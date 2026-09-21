# prob 5 weather analyzer
import datetime
import sys


def read_observations(filename: str):
	observations = {}
	errors = []
	seen = set()
	date_format = "%I:%M:%S %p %m/%d/%Y"

	try:
		with open(filename, "r", encoding="utf-8") as input_file:
			for line_number, line in enumerate(input_file, start=1):
				fields = [field.strip() for field in line.rstrip("\n").split(",")]

				if len(fields) != 3 or any(field == "" for field in fields):
					errors.append((line_number, "malformed line"))
					continue

				station, date, temperature_text = fields

				try:
					temperature = float(temperature_text)
				except ValueError:
					errors.append((line_number, "invalid temperature"))
					continue

				try:
					datetime.datetime.strptime(date, date_format)
				except ValueError:
					errors.append((line_number, "malformed line"))
					continue

				key = (station, date)
				if key in seen:
					errors.append((line_number, "duplicate station/date combination"))
					continue

				seen.add(key)
				observations.setdefault(station, []).append((date, temperature))

	except OSError as error:
		errors.append((0, str(error)))
		return observations, errors

	for records in observations.values():
		records.sort(key=lambda record: datetime.datetime.strptime(record[0], date_format))

	return observations, errors

def station_statistics(observations: dict):
	statistics = {}

	for station, records in observations.items():
		temperatures = [temperature for _, temperature in records]
		statistics[station] = (
			min(temperatures),
			max(temperatures),
			sum(temperatures) / len(temperatures),
		)

	return statistics


def station_outliers(observations: dict):
	statistics = station_statistics(observations)

	return {
		station: (records[-1][0], records[-1][1], statistics[station][2])
		for station, records in observations.items()
		if records and records[-1][1] > statistics[station][2]
	}


def write_statistics(filename: str, statistics: dict):
	with open(filename, "w", encoding="utf-8") as output_file:
		for station in sorted(statistics):
			minimum, maximum, mean = statistics[station]
			output_file.write(
				f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n"
			)


def main():
	if len(sys.argv) != 3:
		print(f"Usage: {sys.argv[0]} input_file output_file")
		return 1

	input_filename, output_filename = sys.argv[1:]
	observations, errors = read_observations(input_filename)

	if errors and errors[0][0] == 0:
		print(f"Unable to read '{input_filename}': {errors[0][1]}")
		return 1

	if errors:
		print("Input errors:")
		for line_number, message in errors:
			print(f"  line {line_number}: {message}")

	statistics = station_statistics(observations)
	outliers = station_outliers(observations)

	print("Statistics:")
	for station in sorted(statistics):
		minimum, maximum, mean = statistics[station]
		print(
			f"  {station}: min={minimum:.1f}, "
			f"max={maximum:.1f}, mean={mean:.1f}"
		)

	print("Outliers:")
	for station in sorted(outliers):
		date, temperature, mean = outliers[station]
		print(f"  {station}: {date}, temperature={temperature:.1f}, mean={mean:.1f}")

	try:
		write_statistics(output_filename, statistics)
	except OSError as error:
		print(f"Unable to write '{output_filename}': {error}")
		return 1

	print(f"Statistics written to '{output_filename}'.")
	return 0


if __name__ == "__main__":
	sys.exit(main())