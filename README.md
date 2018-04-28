# CryptoDataArchitecture

## Sprint01 [Ended at 22/04]
- Done Real-Time Data Schedular.
- Done Integration with DataSet Class
- ~~Integration tests with computed columns~~
## Sprint02 [Ends at 29/04]
### TO-DO
- ~~factor ComputedDataObject and Rule relationship~~
- ~~Integration tests with computed columns~~
- ~~Data Visualisation~~
### Problems Discovered
- Integration between visual tool and DataSet feels a little rushed, might want to go over again
- Current Behaviour is： new data is only pulled in, when all dataset updates are done, maybe able to have it not care about all dataset finishing

## Design Plan and Updated Plan
Both png contains most of the designs.
Updated Plan consists some refactoring and design plans to do this sprint:
- Refactor Rule and DataObject
- Making Computed Columns independent from dataset, logic around notify updates and eventually respond back is a mess
- Visual tool should talk to the system only through dataobjects.

## Plans:
1. Make DataCollector(schedular etc), Data Segment(DataObject, DataSet) and Visual Tool(Not yet implemented) Independent services and should only talk to each other through "contracts" interface/abstract classes
2. Indicators some sort of threshold used to warn of the changes happening to a data column (e.g. set price > 8000 or price < 1000 as points require attention)
3. Signals: represents the signal to enter and exit out of the market, could use one or multiple indicators
4. Indicators and Signals are closely related to eachother and data column, come up with a design for their implementation in sprint03
