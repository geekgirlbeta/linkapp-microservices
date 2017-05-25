"""
A basic indexer service - maintain a list of all items sorted by the date they
were added by the single_endpoint microservice.

Will wait for messages on the queue of the following types:
    
    item.new
    
When it receives a message on the queue, it will update the index. 

If it cannot update the index, it will re-send the message for another worker to 
try again later (not sure if this makes sense, need to work that out).

When successful, it will emit a message of type indexer.success onto the queue.
If it fails, it will emit a message of type indexer.failure onto the queue in addition
to re-sending the original message.
"""

