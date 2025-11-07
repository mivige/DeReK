### Workflow

***

## Detailed Merged Callbot Workflow

### 1. Call Initiation and Introduction

- An incoming call is received by the callbot system.
- The callbot initiates with a scripted introduction and presents options:
    - Transfer immediately to a live agent.
    - Continue with the scripted process.


### 2. Immediate Decision Handling

- Speech-to-text (STT) transcribes the caller’s response for analysis.
    - If the caller requests a transfer:
        - Place in general queue/on hold; process ends here.
    - If speech indicates panic or urgent stress:
        - Caller is assured of immediate transfer to emergency line, then transferred.
    - If caller opts to continue:
        - Proceed to main scripted interaction.


### 3. Request Capture and Sentiment Monitoring (Parallel)

- Callbot verbally asks for caller’s request (using text-to-speech, TTS).
- STT transcribes caller’s spoken request.
- Two large language models (LLMs) operate in parallel:
    - **LLM 1:** Immediately summarizes the transcribed request into a JSON file, capturing essential info.
        - If high frustration is detected at this stage:
            - Caller is assured an agent is being located, transfer is imminent.
            - JSON file is labelled "angry" and sent to necessary department.
            - Attempt direct agent transfer, process ends here.
    - **LLM 2:** Continuously monitors caller sentiment throughout all scripted stages.


### 4. Personal Information Collection (Conditional by Sentiment)

- If caller frustration is **low**:
    - Script proceeds to collect personal information (name, contact, etc.).
    - Responses transcribed and appended to existing JSON file.
- If frustration rises to **medium** during this or a previous stage:
    - Caller is assured an agent from the needed department is being located.
    - Creates and sends a JSON ticket labelled "frustrated" to the department.
    - Skips redundant verification steps; attempts transfer.
- If frustration escalates to **high** at any point:
    - Caller is assured of imminent transfer.
    - JSON ticket is labelled "angry" and sent.
    - Immediate attempt to transfer to the next available agent.


### 5. Readback and Department Confirmation

- Summarized JSON file (request + personal info + department) is read back for caller confirmation (TTS).
    - If corrections are needed:
        - Repeat readback and info collection cycles.
    - If all details confirmed:
        - JSON file sent by email or internal system to relevant department.


### 6. Call Transfer and Ticket Submission Logic

- On confirmation or sentiment-triggered fast-track, check agent availability:
    - If a free agent is found:
        - Transfer caller immediately.
    - If no agent is found:
        - Inform caller a ticket has been submitted to the department:
            - Caller is offered choice to:
                - Stay on the line and wait for the next available agent.
                - Be called back later; caller receives a copy of the ticket (without frustration label unless appropriate).

***

### Workflow Logic Table

| Stage | Actions | Sentiment Handling |
| :-- | :-- | :-- |
| Call Initiation | Introduction \& option: transfer or continue scripted interaction | Immediate transfer if stress detected |
| Request + Sentiment | Capture request via STT \& TTS; LLM summarizes to JSON | Parallel LLM monitoring; high/medium frustration triggers labelled ticket \& agent transfer |
| Personal Info Collection | Collect personal info if frustration is low | Medium frustration triggers transfer and skips re-verification |
| Readback Confirmation | Read back summary and department via TTS | Repeat if info needs correction |
| Agent Transfer/Ticket | Send JSON ticket to department; attempt agent transfer | If no agent, offer wait or callback; ticket sent |


***



