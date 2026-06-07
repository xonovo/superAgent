# Human Queue

Human Queue stores local approval requests created by Runtime V2.6.

Queue items are local operational records and are ignored by Git:

```text
OMCF_Runtime/audit/human_queue/*.json
```

Each queue item has:

1. Runtime run id.
2. Project name.
3. Approval scope.
4. Requester.
5. Approver.
6. Pending status.

The queue turns `WAIT_HUMAN_APPROVAL` from a marker into an explicit approval system.
