# Activity Identities

There is no single onchain number called "people using Solana." We will build an
identity ladder that shows several related truths.

## 1. Fee payer / transaction sender

The wallet that paid for the transaction.

Why it helps: it is a clean way to count initiating wallets.

Why it can mislead: a relayer, embedded wallet service, or sponsor may pay on
someone else's behalf.

## 2. Successful signer

A wallet that authorized a transaction which completed successfully.

Why it helps: failed attempts are removed and authorization is real.

Why it can mislead: one transaction can have several signers, and one person can
control many wallets.

## 3. Application user

A wallet involved in a transaction that invoked a selected application's
programs.

Why it helps: it connects activity to actual products.

Why it can mislead: routers and aggregators can touch several applications in
one transaction. The program-address list becomes part of the definition.

## 4. Likely bot

A wallet whose behavior looks automated: very high frequency, repetitive
instructions, machine-like timing, continuous operation, or linked funding
patterns.

Why it helps: it separates some automation from ordinary product use.

Why it can mislead: this is an estimate, not an identity fact. Humans automate,
and sophisticated bots can imitate humans.

## 5. Likely human-controlled

A wallet whose behavior does not trigger our automation rules and shows more
irregular, varied use.

Why it helps: it creates a more conservative adoption estimate.

Why it can mislead: "not detected as a bot" does not prove a human is present.

## The signal we want

Show all five measurements together, then add retention:

> Did the same wallets return on later days or weeks?

Returning, successful, application-level activity is usually more meaningful
than one large daily wallet count.

## First build slice

Create one Dune result with daily:

- unique fee payers;
- unique successful signers;
- unique users of one selected application;
- the overlap between those groups.

Bot/human classification comes only after the base populations are verified.

