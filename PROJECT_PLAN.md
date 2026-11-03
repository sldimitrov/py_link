# PyLink --- Project Plan

> **Status:** Initial specification\
> **Version:** 0.1.0\
> **Project type:** Educational software engineering project\
> **Primary focus:** Python, networking, real-time messaging,
> concurrency and software architecture

## 1. Project Overview

**PyLink** is a Python-based real-time messaging system that allows
multiple Python clients and browser-based users to communicate through a
centralized server.

The project will begin as a locally hosted application with one shared
chat room. It will provide:

-   A Python backend exposing HTTP endpoints and WebSocket connections.
-   An interactive Python terminal client.
-   A browser-based client implemented with HTML, CSS and Vanilla
    JavaScript.
-   User registration, login and token/session-based authentication.
-   PostgreSQL persistence for users, sessions and messages.
-   A progressive exploration of concurrency concepts, especially
    multithreading.

The project is intentionally designed to grow incrementally. Each
development milestone should introduce a limited number of new concepts,
explain the underlying problem, implement a solution, and verify it with
tests.

### 1.1 Project statement

PyLink is a Python-based real-time messaging system that enables
multiple Python clients and browser-based users to communicate through a
centralized server, with a focus on concurrent programming, networking
and software architecture.

### 1.2 Problem

A real-time chat system must handle multiple connected users, deliver
messages to the correct recipients, preserve message history,
authenticate users and keep different client interfaces consistent.

The engineering challenge is to implement these responsibilities in a
modular way while understanding the concurrency and networking
mechanisms involved.

### 1.3 Main goal

Design, implement and evaluate a modular real-time messaging application
that supports multiple concurrent clients through a Python backend and
provides both terminal and browser interfaces.

## 2. Project Objectives

1.  Build a locally running Python server.
2.  Implement user registration and authentication.
3.  Persist users, sessions and chat messages in PostgreSQL.
4.  Implement a real-time shared chat using WebSockets.
5.  Build an interactive Python CLI client.
6.  Build a browser client using Vanilla JavaScript.
7.  Support simultaneous message sending and receiving.
8.  Introduce multithreading concepts progressively and deliberately.
9.  Test correctness under multiple concurrent connections.
10. Measure latency, throughput and resource usage under increasing
    load.
11. Keep the backend business logic independent of the user interface.
12. Document the architecture, implementation decisions and experimental
    results.

## 3. Scope

### 3.1 MVP --- Initial version

The first usable version will contain:

-   One shared public chat room.
-   Local server deployment.
-   User registration and login through the Python CLI.
-   Separate registration/login through the browser.
-   Persistent user accounts.
-   Token/session-based authentication.
-   Persistent chat message history.
-   Interactive, plain-text Python terminal chat.
-   Browser chat interface.
-   Real-time message delivery through WebSockets.
-   Display of username and message timestamp.
-   Basic validation and error handling.

Both interfaces authenticate independently. They use the same account
system and shared chat history, but the browser does not automatically
inherit the CLI session.

### 3.2 Explicitly out of scope for the first MVP

-   Multiple chat rooms and channels.
-   Direct/private messages.
-   File and image sharing.
-   Message reactions and editing.
-   End-to-end encryption.
-   AI chatbot.
-   Public internet deployment.
-   Rich terminal UI.
-   A public Python SDK.
-   Advanced administration and moderation features.

These are potential future extensions, not MVP requirements.

## 4. Users and Client Interfaces

### 4.1 Python CLI client

The initial Python client is an interactive terminal chat.

Example:

``` text
PyLink — Connected as developer
--------------------------------
[20:15] alice: Hello everyone!
[20:16] bob: Anyone working with Python?

You: Hello! I am testing PyLink.
```

Expected behavior:

-   The user authenticates before connecting to the chat.
-   The client establishes a WebSocket connection.
-   Incoming messages are displayed while the user can continue typing.
-   The user can send messages without leaving the interactive session.
-   The client handles disconnects and connection errors.
-   The initial interface is plain text; no terminal UI framework is
    required.

The interactive client will eventually provide a practical exercise in
coordinating input and network receiving. A possible implementation is a
main thread for terminal input and a background receiver thread for
incoming WebSocket messages. The exact implementation will be introduced
and tested in the relevant concurrency milestone.

### 4.2 Browser client

The browser client will use:

-   HTML for structure.
-   CSS for presentation.
-   Vanilla JavaScript for behavior.
-   HTTP for registration, login and message-history requests.
-   WebSocket for real-time message exchange.

The browser has its own login flow. It does not automatically receive or
reuse the Python CLI token.

### 4.3 Future Python SDK

A Python SDK is a possible later extension. It would allow other Python
applications to connect to PyLink programmatically.

Illustrative future API:

``` python
from pylink import Client

client = Client("http://127.0.0.1:8000")
client.connect(token="...")
client.send_message("Hello from another application!")
```

This is an example of a future interface, not a committed MVP API.

## 5. Proposed Technology Stack

  -----------------------------------------------------------------------
  Area                    Technology              Responsibility
  ----------------------- ----------------------- -----------------------
  Language                Python 3.12+            Backend and Python
                                                  clients

  Backend framework       FastAPI                 HTTP API and WebSocket
                                                  endpoints

  ASGI server             Uvicorn                 Runs the FastAPI
                                                  application

  Database                PostgreSQL              Persistent application
                                                  data

  ORM                     SQLAlchemy 2.x          Database mapping and
                                                  queries

  Migrations              Alembic                 Versioned database
                                                  schema changes

  Browser                 HTML, CSS, Vanilla      Web interface
                          JavaScript              

  Real-time transport     WebSocket               Bidirectional chat
                                                  communication

  Python HTTP client      HTTPX                   CLI HTTP requests

  Python WebSocket client To be selected during   CLI real-time
                          implementation          connection

  Testing                 pytest                  Automated tests

  Async testing           pytest-asyncio, where   Asynchronous tests
                          needed                  

  Local infrastructure    Docker Compose,         Reproducible PostgreSQL
                          optional                environment
  -----------------------------------------------------------------------

### 5.1 Why FastAPI and Uvicorn?

FastAPI provides the application framework: routes, request validation,
dependency injection and WebSocket endpoint support.

Uvicorn is an ASGI server that runs the FastAPI application and accepts
network connections. It is not a replacement for FastAPI; the two have
different responsibilities.

ASGI supports asynchronous application patterns and long-lived
connections such as WebSockets. This gives the project a practical
foundation for real-time communication.

### 5.2 Async and multithreading are different concepts

FastAPI and Uvicorn commonly use asynchronous I/O for handling many
network connections. This does not mean that multithreading is
automatically being used for every request.

PyLink will distinguish and study:

-   Sequential execution.
-   Thread-based concurrency.
-   Asynchronous I/O and the event loop.
-   Thread-safe communication and synchronization.
-   Producer-consumer queues.
-   The practical differences between concurrency models.

The project must not introduce threads merely to claim that it uses
multithreading. Each use of concurrency should solve a clearly
identified problem and be supported by tests or measurements.

## 6. High-Level Architecture

The system consists of three primary parts:

1.  **Backend server:** owns application rules, authentication, message
    routing and persistence.
2.  **Python CLI client:** provides terminal-based access.
3.  **Browser client:** provides web-based access.

Both clients communicate with the same backend and use the same user and
message data.

``` mermaid
flowchart TB
    CLI[Python CLI Client]
    WEB[Browser Client<br/>HTML / CSS / JavaScript]

    subgraph SERVER[PyLink Backend]
        API[FastAPI HTTP API]
        WS[WebSocket Endpoint]
        AUTH[Authentication]
        CHAT[Chat and Message Services]
        HUB[Connection Manager]
        REPO[Persistence Layer]
    end

    DB[(PostgreSQL)]

    CLI -->|HTTP: register / login| API
    CLI <-->|WebSocket: chat| WS

    WEB -->|HTTP: register / login / history| API
    WEB <-->|WebSocket: chat| WS

    API --> AUTH
    API --> CHAT
    WS --> AUTH
    WS --> HUB
    HUB --> CHAT
    CHAT --> REPO
    AUTH --> REPO
    REPO --> DB
```

### 6.1 Architectural responsibilities

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  HTTP API                            Registration, login and history
                                      endpoints

  WebSocket endpoint                  Authenticated real-time connections

  Authentication service              Password verification and session
                                      validation

  Chat service                        Message validation and application
                                      rules

  Connection manager                  Tracks active WebSocket connections

  Persistence layer                   Reads and writes application data

  PostgreSQL                          Stores persistent records

  CLI client                          Terminal interaction and server
                                      communication

  Browser client                      Web interaction and server
                                      communication
  -----------------------------------------------------------------------

The connection manager should be separate from the chat service. The
chat service should not need to know whether a message originated from a
terminal or a browser.

## 7. Communication Model

### 7.1 HTTP responsibilities

HTTP will initially handle:

-   User registration.
-   User login.
-   Retrieving chat history.
-   Health/status checks.

### 7.2 WebSocket responsibilities

WebSocket will handle:

-   Establishing an authenticated chat connection.
-   Sending messages.
-   Receiving broadcast messages.
-   Handling connection closure.

### 7.3 Initial message lifecycle

``` mermaid
sequenceDiagram
    participant A as Client A
    participant S as PyLink Server
    participant DB as PostgreSQL
    participant B as Client B

    A->>S: Send message
    S->>S: Validate message and session
    S->>DB: Persist message
    DB-->>S: Message stored
    S->>A: Broadcast message
    S->>B: Broadcast message
    B-->>B: Display message
```

The intended initial behavior is to persist a valid message before
broadcasting it. This avoids broadcasting a message that the application
failed to store.

The final implementation must define how database failures and
disconnected recipients are handled.

## 8. Authentication and Security

### 8.1 Account registration

A user registers with a username and password.

Passwords must never be stored in plaintext. A dedicated
password-hashing implementation should be selected during the
authentication milestone. Argon2id is the preferred candidate.

### 8.2 Login and sessions

After successful authentication:

-   The server creates an authenticated session.
-   The CLI receives a token and stores it locally with appropriate file
    permissions.
-   The browser receives its own authenticated session.
-   The server can invalidate sessions.
-   Token expiration and logout behavior must be defined and tested.

A database-backed opaque random token is a candidate for the initial
implementation. The server should store a hash of the token rather than
the raw token.

### 8.3 Browser authentication

The browser will have a separate login form and session.

An HttpOnly cookie is the preferred browser-session mechanism for the
initial web implementation. Cookie security settings, SameSite policy
and CSRF considerations must be defined when implementing
authentication.

### 8.4 WebSocket authentication

The WebSocket connection must be authenticated before the user can send
or receive chat messages.

Do not put long-lived authentication tokens in ordinary URLs or query
strings, because URLs may be logged or exposed through other mechanisms.
Select an appropriate browser-compatible authentication handshake during
implementation.

### 8.5 Future security work

-   HTTPS for non-local deployment.
-   More complete session management.
-   Rate limiting.
-   Input validation and abuse prevention.
-   Encryption of stored data where appropriate.
-   Evaluation of end-to-end encryption as a separate, advanced feature.

TLS transport encryption and end-to-end encryption are different
security properties and must not be treated as interchangeable.

## 9. Initial Data Model

The first database schema is expected to contain three core entities.

### 9.1 users

  Field           Purpose
  --------------- ----------------------------
  id              Primary key
  username        Unique username
  password_hash   Password hash
  created_at      Account creation timestamp

### 9.2 sessions

  Field        Purpose
  ------------ -------------------------------
  id           Primary key
  user_id      Reference to user
  token_hash   Hash of issued token
  created_at   Session creation timestamp
  expires_at   Session expiration
  revoked_at   Optional revocation timestamp

### 9.3 messages

  Field        Purpose
  ------------ -------------------
  id           Primary key
  user_id      Message author
  content      Message text
  created_at   Message timestamp

The exact PostgreSQL types, constraints, indexes, deletion policies and
migration definitions will be designed during implementation.

Potential future entities include `chat_rooms`, `room_members` and
`message_reactions`.

## 10. Concurrency Learning and Implementation Strategy

Concurrency is a central learning and research objective, but it will be
introduced incrementally.

### Stage 1 --- Sequential baseline

Build the simplest working message flow. Understand the lifecycle of a
connection and a message before adding concurrency mechanisms
explicitly.

### Stage 2 --- Multiple connections

Support multiple simultaneous WebSocket clients. Introduce the
connection manager and understand how the ASGI event loop handles
concurrent I/O.

### Stage 3 --- Python CLI input and receiving

Implement simultaneous terminal input and network receiving. Explore a
background receiver thread and the main input thread.

### Stage 4 --- Thread safety

Identify shared mutable state. Introduce locks only where needed and
demonstrate the race condition or inconsistency they prevent.

### Stage 5 --- Producer-consumer pattern

Introduce a thread-safe queue for decoupling message production from
message processing. Define ownership, queue behavior and shutdown
handling.

### Stage 6 --- Background workers

Explore background processing for suitable tasks. Keep database sessions
and other resources scoped safely to the execution context that uses
them.

### Stage 7 --- Compare concurrency models

Compare selected thread-based and asynchronous implementations under
controlled conditions. Document workload, environment, methodology and
limitations.

Important: FastAPI's asynchronous server model and a threaded CLI client
are separate concerns. Adding threads to the CLI does not make the
server thread-based. Any server-side thread pool or worker design must
be justified independently.

## 11. Development Roadmap

Each milestone should result in a working, testable increment.

  -----------------------------------------------------------------------
  Milestone               Deliverable             Main learning topics
  ----------------------- ----------------------- -----------------------
  M0                      Repository and          Git, packaging, virtual
                          development environment environments

  M1                      Minimal FastAPI server  HTTP, ASGI, Uvicorn

  M2                      PostgreSQL integration  SQL, SQLAlchemy,
                                                  Alembic

  M3                      Registration and login  Password hashing,
                                                  sessions, tokens

  M4                      First Python HTTP       HTTP requests,
                          client                  client-server model

  M5                      Basic WebSocket         Persistent connections,
                          endpoint                protocol lifecycle

  M6                      Shared chat and         Message flow,
                          persistence             connection management

  M7                      Interactive Python      Input/output
                          terminal chat           coordination

  M8                      Browser login and chat  JavaScript, DOM,
                                                  browser WebSocket

  M9                      Concurrency             Threads, locks, queues,
                          improvements            synchronization

  M10                     Automated integration   Test clients, multiple
                          tests                   connections

  M11                     Performance experiments Latency, throughput,
                                                  profiling

  M12                     Documentation and       Diagrams, analysis,
                          course-work material    conclusions
  -----------------------------------------------------------------------

The order may be adjusted when implementation reveals dependencies. Each
milestone should have explicit acceptance criteria before work begins.

## 12. Testing Strategy

### 12.1 Unit tests

Test isolated application behavior:

-   Username and message validation.
-   Password hashing and verification.
-   Session creation and validation.
-   Message service behavior.
-   Connection manager behavior.

### 12.2 Integration tests

Test interactions between components:

-   Registration and login.
-   Database persistence.
-   Authenticated WebSocket connection.
-   Sending and receiving messages.
-   Message history retrieval.
-   Disconnect and reconnect behavior.

### 12.3 Concurrency tests

Test scenarios such as:

-   Multiple clients connecting simultaneously.
-   Multiple clients sending messages at approximately the same time.
-   A client disconnecting during message delivery.
-   Repeated connect/disconnect cycles.
-   Correct delivery without unintended message duplication.

### 12.4 Performance experiments

Measure:

-   Message round-trip latency.
-   Message throughput.
-   Connection establishment time.
-   Server CPU and memory usage.
-   Behavior under increasing concurrent client counts.

Initial experiment targets may include 10, 50, 100 and 500 simulated
clients, subject to available hardware and test reliability.

The measurements must be reported as experimental results, not assumed
performance guarantees.

## 13. Future Enhancements

These features are intentionally excluded from the first MVP.

### Client and interface improvements

-   Rich-based terminal formatting.
-   Textual terminal UI with panels and interactive components.
-   Additional CLI commands: `send`, `history`, `users`, `profile`,
    `disconnect`.
-   Python SDK for external applications.
-   Improved browser UI.

### Messaging features

-   Multiple chat rooms.
-   Direct/private messages.
-   User presence and online status.
-   Message reactions.
-   File sharing.

### Advanced engineering

-   LAN deployment.
-   Public deployment on a VPS.
-   TLS and hardened session management.
-   More advanced encryption, potentially end-to-end encryption.
-   Redis-backed message distribution if multi-process or multi-instance
    deployment requires it.

### AI integration

An AI chatbot is a possible extension. Its purpose and implementation
are not yet selected.

Potential directions include:

-   Python programming assistant.
-   Knowledge assistant using retrieval-augmented generation (RAG).
-   Chat moderation assistant.
-   Custom-purpose bot that participates in the shared chat.

AI integration should be considered only after the core messaging system
is stable.

## 14. Documentation and Academic Deliverables

The project should support both software development and the university
course-work requirements.

Planned documentation:

-   Project overview and objectives.
-   Functional and non-functional requirements.
-   Architecture diagrams.
-   Message-flow and client-lifecycle diagrams.
-   Database schema / ER diagram.
-   Threading and concurrency diagrams.
-   API and WebSocket protocol documentation.
-   Setup and usage instructions.
-   Test cases and benchmark methodology.
-   Experimental results and conclusions.
-   References to technical documentation and libraries.

The academic report can be organized into:

1.  Introduction --- problem, motivation, goal and tasks.
2.  Main section --- architecture, algorithms, technologies,
    implementation and experiments.
3.  Conclusion --- achieved results, limitations and lessons learned.
4.  References --- documentation, libraries and other sources used.

## 15. Proposed Repository Structure

The following is a starting proposal. Directories should be created when
their corresponding implementation work begins; avoid creating empty
modules without a clear responsibility.

``` text
pylink/
├── README.md
├── PROJECT_PLAN.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── websocket-protocol.md
│   ├── database.md
│   ├── diagrams/
│   │   ├── system-architecture.mmd
│   │   ├── message-flow.mmd
│   │   └── threading-model.mmd
│   └── research/
│
├── src/
│   └── pylink/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       ├── auth/
│       ├── chat/
│       ├── clients/
│       │   └── cli/
│       ├── database/
│       ├── models/
│       └── services/
│
├── web/
│   ├── index.html
│   ├── login.html
│   ├── css/
│   └── js/
│
├── migrations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── benchmarks/
│
└── examples/
```

## 16. Development Principles

1.  **Incremental learning:** introduce one major concept at a time.
2.  **Understand before abstracting:** prefer a clear implementation
    over premature abstractions.
3.  **Separation of concerns:** keep transport, business logic,
    persistence and presentation separate.
4.  **Test every milestone:** new behavior must have appropriate tests.
5.  **Document decisions:** record meaningful architectural decisions
    and their trade-offs.
6.  **Measure performance:** do not make concurrency or scalability
    claims without experiments.
7.  **Keep the MVP small:** future features must not block the first
    working chat.
8.  **Security by design:** never store plaintext passwords or expose
    long-lived tokens unnecessarily.

## 17. Open Decisions

The following points remain to be finalized during implementation:

-   Exact Python version and dependency versions.
-   Exact password-hashing package and session-token format.
-   Browser session and CSRF implementation details.
-   Python WebSocket client library.
-   Exact CLI token storage location and permissions.
-   Database transaction and message-delivery failure behavior.
-   WebSocket message schema and error protocol.
-   Reconnection and message ordering guarantees.
-   Whether and when server-side background threads are justified.
-   Final benchmark tooling and workload.
-   AI chatbot purpose and library.

These are intentionally open. They should be resolved when the relevant
milestone provides enough context to make an informed decision.

## 18. Definition of MVP Completion

The MVP is considered complete when:

-   The developer can start the local backend and PostgreSQL
    environment.
-   A user can register and log in through the Python CLI.
-   A user can register and log in separately through the browser.
-   Both interfaces can connect to the same shared chat.
-   A message sent by one connected user is delivered to other connected
    users.
-   Messages are persisted in PostgreSQL.
-   A user can retrieve previous chat messages after reconnecting.
-   Basic authentication and validation tests pass.
-   The project has setup instructions and architecture documentation.

------------------------------------------------------------------------

**Initial project direction:** Build a small, working real-time chat
first. Then use it as a controlled environment for studying networking,
multithreading, synchronization, asynchronous I/O and performance.
