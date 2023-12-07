from almanac.Almanac import Almanac

def main():
    almanac = Almanac('example-1.txt', 'range')

    min_location = None
    for location in almanac.get_locations():
        if min_location is None or location < min_location:
            print(f'Found new lowest location {location}')
            min_location = location

    print('Lowest location:', min_location)

if __name__ == '__main__':
    main()
