# DNS Protocol Notes

##   DNS Request Query
### Transaction ID - 2 Bytes
### Flags - 2 Bytes
### Questions - 2 Bytes
### Answer RRs - 2 Bytes
### Authority RRs - 2 Bytes
### Additional RRs - 2 Bytes
### Name:
#### Length(Sub-Domain)
#### Sub-Domain
#### Length(Domain)
#### Domain
#### Length(TLD)
#### TLD
### Type - 2 Bytes
### Class - 2 Bytes

TODO

##   DNS Response Query
#### Transaction ID - 2 Bytes
#### Flags - 2 Bytes
### Questions - 2 Bytes
### Answer RRs - 2 Bytes
### Authority RRs - 2 Bytes
### Additional RRs - 2 Bytes
### Queries:
#### Question Name:
##### Question Length(Sub-Domain)
##### Question Sub-Domain
##### Question Length(Domain)
##### Question Domain
##### Question Length(TLD)
##### Question TLD
#### Question Type - 2 Bytes
#### Question Class - 2 Bytes
### Answers: 
#### Answer Name:
##### Answer Name = \xc0\x0c (Pointer To Question Name Domain) - 2 Bytes
##### Answer Type - 2 Bytes
##### Answer Class - 2 Bytes
##### Answer TTL - 4 Bytes
##### Answer Data Length - 2 Bytes
##### Answer Address - Answer Data Length Bytes