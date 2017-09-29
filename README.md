# Signal_iQ

Signal iQ is an SDK that allows for variety of "signals" (events, alerts, SLA violations, Ux events, etc.) to be sent as a signal to SIOS iQ Machine Learning platform for correlation.
Signals will be correlated to the incidents (created via Topological Behaviour Analysis) and summarized into problems (via MetaAnalysis) as well as presented to the users via SIOS iQ UI and APIs.

Such signals are implemented in variety of programming and scripting languages (such as python, C++, C#, javascript, etc.).

# Prerequisites

There are a two prerequisites for injection that are common to all Signals (independent of the language):

* Environment id
* Virtual Machine UUID

This section will cover where such can be obtained manually (through UI) and/or programmatically.

## How do I get the environment id?
1. Please make sure you are running SIOS iQ 3.13 or later.
2. There are two ways to obtain the environment id:
  (a) SIOS iQ user interface by accessing Inventory -> Environment of Interest -> Properties where ID will appear right under the name of the environment.
  (b) Another approach is a programmatic approach by sending the GET request to https://<ip or FQDN>/api/sios/stc/cldo/environment 

JSON output:

```
  environment: [6]
  0: Object
  id: 500
  name: "------"
  description: ""
  healthState: "-----"
  .......
```

## How do I get VM's UUID?

1. Use virtualisation/cloud provider's tool (such as: vCenter)
2. Programmatically  by sending the GET request to https://<ip or FQDN>/api/sios/stc/cldo/vm
This will return all VMs and one of the properties will be UUID. If you know a specific VM name or other properties to make the list much small and/or specific, then you can use filtering capabilities of the API

### Filtering
The filtering syntax is best shown by the examples in the table below.  A query parameter called filter is used and its value is an expression based on the operators shown below.

| Operator                      | Description                                                  | Example                                         |
| ----------------------------- | ------------------------------------------------------------ | ----------------------------------------------- |
| Logical and Boolean Operators |
|                               |                                                              |                                                 |
| eq                            | Equal                                                        | /Suppliers?filter=Address.City eq 'Redmond'     |
| ne                            | Not equal                                                    | /Suppliers?filter=Address.City ne 'London'      |
| gt                            | Greater than                                                 | /Products?filter=Price gt 20                    |
| ge                            | Greater than or equal 	/Products?filter=Price ge 10         |
| lt                            | Less than 	/Products?filter=Price lt 20                     |
| le                            | Less than or equal 	/Products?filter=Price le 100            |
| and                           | Logical and 	/Products?filter=Price le 200 and Price gt 3.5 |
| or                            | Logical or 	/Products?filter=Price le 3.5 or Price gt 200    |
| not                           | Logical negation 	/Products?filter=not Price eq 100          |
|                               |                                                              |                                                 |
| Grouping Operators            |
|                               |                                                              |                                                 |
| ( )                           | Precedence grouping                                          | /Products?filter=(Price lt 5) and (Price gt 2)  |
| String-specific Operators     |
|                               |                                                              |                                                 |
| like                          | string contains                                              | /Suppliers?filter=Address.City like 'ville'     |
| ilike                         | case-insensitive string contains                             | /Suppliers?filter=Address.County ilike 'lexing' |
| Set Operators                 |
|                               |                                                              |                                                 |
| contains                      | Collection contains (specify ID of contained object)         | /Stores?filter=ProductList contains 42#.        |
