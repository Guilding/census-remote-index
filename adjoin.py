import csv, sys

if __name__ == '__main__':
    out_path, geo_path, other_paths = sys.argv[1], sys.argv[2], sys.argv[3:]

    print('Adjoining', out_path, 'from', geo_path, 'and',
           len(other_paths), 'other files', file=sys.stderr)

    geo_csv = csv.reader(open(geo_path, encoding='Latin-1'))

    moe_starts_at = len(other_paths) // 2
    (estimate_paths, moe_paths) = (other_paths[:moe_starts_at], other_paths[moe_starts_at:])
    estimate_readers = []
    moe_readers = []

    for (estimate_path, moe_path) in zip(estimate_paths, moe_paths):
        estimate_readers.append(csv.reader(open(estimate_path, encoding='Latin-1')))
        moe_readers.append(csv.reader(open(moe_path, encoding='Latin-1')))

    with open(out_path, 'w', encoding='Latin-1') as out_file:
        out = csv.writer(out_file)

        for geo_row in geo_csv:
            out_row = geo_row[:]

            for (estimate_reader, moe_reader) in zip(estimate_readers, moe_readers):
                # Pull one line out of each estimate and moe CSV and chop off the first six fields
                estimates_for_geo = next(estimate_reader)[6:]
                moes_for_geo = next(moe_reader)[6:]

                # Zip the estimates and MOEs together and extend the output with that estimate,moe,estimate,moe,… data
                for estimate, moe in zip(estimates_for_geo, moes_for_geo):
                    out_row.append(estimate)
                    out_row.append(moe)

            out.writerow(out_row)
