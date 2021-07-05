[![Updates](https://pyup.io/repos/github/amor71/mnqueues/shield.svg)](https://pyup.io/repos/github/amor71/mnqueues/)
[![Python 3](https://pyup.io/repos/github/amor71/mnqueues/python-3-shield.svg)](https://pyup.io/repos/github/amor71/mnqueues/)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

# What are mnqueues?

`mnqueues` stands for Monitored Queues - a coupling between a Queue and a Monitor entity. An abstract Queue is a means for two, or more end points to exchange data. A Monitor collect and alerts on Queue usage statistics. 

For example, a Queue may be a multiprocessing.Queue, used for asynchronous exchange of data between two processes, and Monitor alerts when the rate of production is higher than rate of consumption, indicating performance issues on the consumer side.

## Tracked measures

`mnqueues` tracks several measures per queue:

1. Average number of writes to queue per minute,
2. Average number of reads to queue per minute,

## Supported monitoring systems

1. GCP (StackDriver)

## Contributing

Contributions are highly appreciated. Please review our 
[Code of Conduct](https://github.com/amor71/mnqueues/blob/master/CODE_OF_CONDUCT.md). Bug reports & feature requests can be left in the `Issues` section, or email me at amor71@sgeltd.com


