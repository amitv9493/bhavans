import csv

from registration.models import Registration


def main():
    with open("Baa-Registration.csv", "r") as file:
        reader = csv.reader(file)
        list_of_object = []
        for row in reader:
            list_of_object.append(
                Registration(
                    id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                )
            )
        Registration.objects.bulk_create(list_of_object)

        # print(
        #     type(row[0]),
        #     type(row[1]),
        #     type(row[2]),
        # )
        # print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], sep="|) ")


# The `main()` function is responsible for reading data from a CSV file named "Baa-Registration.csv"
# and creating `Registration` objects in the database using the data from the CSV file.
# main()
