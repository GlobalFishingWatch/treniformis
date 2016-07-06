# Classification lists

* This directory `classification_lists` contains lists of vessels with very high
  quality, likely human-verified labels.
* Each csv file can have many columns, but one column must contain mmsis, and
  another must contain a label for that vessel.
* The current vessel types are supported for classification:
  * Fishing
    * Longliner
    * Trawler
    * Purse seine
    * Fish carrier
    * Pole and line
  * Non-fishing
    * Cargo
    * Passenger (including cruise ships, sailing vessels, ferries and other pleasure craft).
    * Tugs (including pilot vessels).
    
## Criteria for adding a new file

* The labels must be of very high quality, e.g. we are confident that the accuracy is 95% or higher.
* Types outside the list above can be included in the file (and will be ignored for now), but for
  vessels that match the supported list, there must be a clear mapping from the labels in the csv
  file to these canonical types.
