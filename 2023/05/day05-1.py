from almanac.Almanac import Almanac

def main():
    almanac = Almanac('data.txt')

    locations = almanac.get_locations()

    print('Lowest location:', min(locations))

if __name__ == '__main__':
    main()
