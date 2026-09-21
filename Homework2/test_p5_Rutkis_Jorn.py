import tempfile
import unittest
from pathlib import Path

from p5_Rutkis_Jorn import (
	read_observations,
	station_statistics,
	write_statistics,
)


class WeatherAnalyzerTests(unittest.TestCase):
	def test_stations_and_negative_temperatures(self):
		with tempfile.TemporaryDirectory() as directory:
			input_path = Path(directory) / "observations.csv"
			input_path.write_text(
				"North,09:00:00 AM 04/20/2026,-5.5\n"
				"South,10:00:00 AM 04/20/2026,12.0\n",
				encoding="utf-8",
			)

			observations, errors = read_observations(str(input_path))

		self.assertEqual(errors, [])
		self.assertEqual(observations["North"][0][1], -5.5)
		self.assertIn("South", observations)

	def test_duplicate_observations(self):
		with tempfile.TemporaryDirectory() as directory:
			input_path = Path(directory) / "duplicates.csv"
			input_path.write_text(
				"North,09:00:00 AM 04/20/2026,10\n"
				"North,09:00:00 AM 04/20/2026,11\n",
				encoding="utf-8",
			)

			observations, errors = read_observations(str(input_path))

		self.assertEqual(len(observations["North"]), 1)
		self.assertEqual(
			errors,
			[(2, "duplicate station/date combination")],
		)

	def test_invalid_date_and_temperature(self):
		with tempfile.TemporaryDirectory() as directory:
			input_path = Path(directory) / "invalid.csv"
			input_path.write_text(
				"North,09:00:00 AM 04/31/2026,10\n"
				"South,10:00:00 AM 04/20/2026,not-a-number\n",
				encoding="utf-8",
			)

			observations, errors = read_observations(str(input_path))

		self.assertEqual(observations, {})
		self.assertEqual(
			errors,
			[(1, "malformed line"), (2, "invalid temperature")],
		)

	def test_calculated_statistics(self):
		observations = {
			"North": [
				("09:00:00 AM 04/20/2026", -5.0),
				("10:00:00 AM 04/20/2026", 10.0),
				("11:00:00 AM 04/20/2026", 4.0),
			]
		}

		self.assertEqual(
			station_statistics(observations),
			{"North": (-5.0, 10.0, 3.0)},
		)

	def test_sorted_statistics_output(self):
		statistics = {
			"South": (1.0, 3.0, 2.0),
			"North": (-5.0, 10.0, 2.5),
		}

		with tempfile.TemporaryDirectory() as directory:
			output_path = Path(directory) / "statistics.csv"
			write_statistics(str(output_path), statistics)

			self.assertEqual(
				output_path.read_text(encoding="utf-8"),
				"North,-5.0,10.0,2.5\nSouth,1.0,3.0,2.0\n",
			)

	def test_missing_file(self):
		observations, errors = read_observations("file_that_does_not_exist.csv")

		self.assertEqual(observations, {})
		self.assertEqual(len(errors), 1)
		self.assertEqual(errors[0][0], 0)
		self.assertTrue(errors[0][1])


if __name__ == "__main__":
	unittest.main()
