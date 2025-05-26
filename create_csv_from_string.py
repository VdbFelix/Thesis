import csv

martyrs_name = "Aron.Abdas.Abdiesus.Abdon.Abedecalaas"
martyrs_list = martyrs_name.replace(".", ",")

martyrs_csv = [martyrs_list]

with open('1576_martyrs_list.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    for line in martyrs_csv:
        for item in line.split(","):
            my_writer.writerow([item.strip()])
