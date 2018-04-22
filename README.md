# CryptoDataArchitecture

## Sprint01 [Ended at 22/04]
- Done Real-Time Data Schedular.
- Done Integration with DataSet Class
- ~~Integration tests with computed columns~~
## Sprint02 [Ends at 29/04]
- Refactor ComputedDataObject and Rule relationship
- Integration tests with computed columns
- Data Visualisation

## Design Plan and Changed Plan
Both png contains most of the designs.
Changed Plan consists some refactoring and design plans to do this sprint:
- Refactor Rule and DataObject
- Visual tool should talk to the system only through dataobjects.

## Plans:
1. Make DataCollector(schedular etc), Data Segment(DataObject, DataSet) and Visual Tool(Not yet implemented) Independent services and should only talk to each other through "contracts" interface/abstract classes
2. Indicators some sort of threshold used to warn of the changes happening to a data column (e.g. set price > 8000 or price < 1000 as points require attention)
3. Signals: represents the signal to enter and exit out of the market, could use one or multiple indicators
4. Indicators and Signals are closely related to eachother and data column, come up with a design for their implementation in sprint03
