#!/usr/bin/env python

from PayloadQueue import PayloadQueue


pq = PayloadQueue()

print( pq.isBacklogPresent() )
print( pq.getPayload() )
pq.deleteLastPayload()
print( pq.getPayload() )
