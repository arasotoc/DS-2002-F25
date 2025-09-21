.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "fetching METAR data..."
	./fetch_metars.sh
	@echo "Fetch complete!"
analyze: fetch
	@echo "Analyzing METAR data..."
	./analyze_data.sh
	@echo "Analyzsis complete!Data saved to weather_report.csv"

clean:
	@echo "Cleaning up..."
	rm -rf raw_metars weather_report.csv
	@echo "Cleanup done!"
