Cleaning up raw data pulled from a Hacker News salary survey conducted on 3/21/16. Latest clean version of the data is available [here](https://docs.google.com/spreadsheets/d/1HgANr81Ako1AiipJYqdIKkKDz_TaFBjS-F4psmF3N6M/edit?usp=sharing).

## Additional Information

* [Hacker News thread](https://news.ycombinator.com/item?id=11331223) 
* [Google Sheet of survey responses](https://docs.google.com/spreadsheets/u/1/d/1a1Df6dg2Pby1UoNlZU2l0FEykKsQKttu7O6q7iQd2bU/htmlview?usp=sharing&sle=true)

## External data sources

* [US and Canadian states](http://statetable.com/)
* [Countries](https://mledoze.github.io/countries/)
* [Zip Codes](http://federalgovernmentzipcodes.us/)
* Google provided currency conversion rates

## Notes on validation

* No responses were removed for trolling. Luckily, imposing sane limits on some fields eliminated a lot of them.
* Currency conversion is hard when no one indicates the currency being used. Right now, rows indicating a currency type other than USD are converted to USD and everything else is assumed to be USD. Salary analysis internationally is sketchy at best.
