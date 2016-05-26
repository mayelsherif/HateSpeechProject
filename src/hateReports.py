from bs4 import BeautifulSoup
import requests



def writeTSVFile(fileName, header, data):
    f = open(fileName, 'w')
    print >> f, header
    for row in data:
        print >> f, row.encode('utf8')
    f.close()

if __name__ == '__main__':
    # As of Wed May 25th, No hate speech movements has 47 pages of reports, each has 10 reports
    reportPage_cnt = 47
    cnt = 1
    tsv_data = list()

    for i in range(1, reportPage_cnt+1): # will do url1, url2, ....url(reportPage_cnt)
        url = "http://www.nohatespeechmovement.org/hate-speech-watch/report/" + str(i)
        r  = requests.get(url)
        data = r.text

        soup = BeautifulSoup(data)
        reports = soup.find_all("div", {"class:", "report-entry"})
        #print reports


        # Form the tab seperated file: report_title \t report_link \t lang \t report_desc \t author_info \t tags
        # 6 pieces of info related to each report


        for report in reports:
                report_list = list()

                #print(report.contents[1].find_all(("div", {"class:", "report-screenshot-box"})))
                print ("Report" + str(cnt) + "********************************************")

                #get the title of the report
                report_title = report.contents[3].find_all("a")[0].text.strip()
                #print(report_title)
                report_list.append(report_title)


                #get the report link
                report_link = report.contents[5].find_all("a", {"class:", "fancy"})[0]["href"]
                #print(report_link)
                report_list.append(report_link)

                #get the language and the report text from [7]
                lang = report.contents[7]["lang"]
                #print(lang)
                report_list.append(lang)
                # the report content
                report_desc = " ".join(report.contents[7].get_text().strip().split())
                #print(report_desc)
                report_list.append(report_desc)

                #get author information from [9] name, country and date

                author_country_date = " ".join(report.contents[9].get_text().strip().split())
                author_info = author_country_date[11:] #skip the Report by: substring
                #print(author_info)
                report_list.append(author_info)

                #get the tags associated with the report: We can use this for labeling
                tags = []
                try:
                    for tag in report.contents[11].find_all("span", {"class:", "tag"}):
                        tags.append(tag.get_text().strip())
                except:
                    pass

                report_tags = ", ".join(tags)
                report_list.append(report_tags)

                report_line = "\t".join(report_list)
                tsv_data.append(report_line)
                print report_list
                print len(report_list)
                cnt = cnt +1

        #for report in reports:
        #    print reports.content
        #print len(reports)
    header_content = ["report_title", "report_link", "lang", "report_desc", "author_info", "tags"]
    header = "\t".join(header_content)
    writeTSVFile("HateSpeechReports.tsv",header, tsv_data)
        #print soup.prettify()

        #for link in soup.find_all('a'):
        #    print(link.get('href'))