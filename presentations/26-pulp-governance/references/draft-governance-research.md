# Governance Research

Thanks for the input, that makes sense to me.
Sponsorship doesn't feel right wording.

But let's take a step back, I'm afraid my original idea on the sponsorship page was an [XY problem](https://en.wikipedia.org/wiki/XY_problem) (sorry about that).
The original ask that motivated my question was a user feedback that it was not clear the company behind the project, so I would call that a governance documentation problem (after some research motivated by this conversation!).

So what we really want is not a sponsors page, is to describe 

We do have some governance documents in the site and repositories, but not on this.
Pulp is owned

## Goal

Explicitly define the Pulp Project governance model.

## Motivation

TLDR: explicit governance is good for our community health.
Citing the open-source-way handbook:

> Clear and explicit governance models have another critical benefit—cultivating a strong sense of trust in your project's community. Members of projects with robust, detailed governance models benefit from a shared commitment to a transparent set of procedures, policies, and role descriptions. They can appeal to a commonly understood set of guidelines when disputes arise. All of this makes questions about participants' motives, intentions, goals, and authority less contentious. [^1]

## Development

### What is governance

### Some archeology

Kind by chance, I found this [Pulp community health audit] blog post.


### Pulp's current governance operation

The goal of this document is to write a clear governance document,
but before that, I want to discuss and describe how the project currently operates.

According to the types of governance models described in The Open Source Way [^2],
Pulp fits mainly in the corporate-baked spectrum.
The main characteristtic are:
- The organization owners in the hosting platform (GitHub) are all red hatters.
- Code changes of core components must have a red hatter approval.
- Ultimately, the vision and important decisions are made by red hatters

On the other hand, it's also fair to point that the project, as it currently operates,
is open to dialogue, contributions and partnerships.
Some examples:
- We provide best-effort support to community issues and feature requests
- We provide best-effort reviews for outside contributors, specially partners

### Draft

#### NextJS

The [NextJs governance document] shows:

> Next.js was created by the team at Vercel
in 2016.
> 
>  The research and development of Next.js is led by the core team working full-time at Vercel. With over 3,000 contributors from around the world, Next.js is a collaborative open-source effort to build tools for React and Web developers.

The teams further clarifies that the core team is Vercel and there are collaborator teams from Google and Meta.

#### CNCF

https://contribute.cncf.io/community/governance/

#### Gitea

The [gitea] project is corporate-backed and has the footer lines:

> Gitea is open source, with leadership and commercial support from CommitGo.

#### Forjeo

The [forjeo] project has a governance repository.
Lots of interesting stuff there about managing a community project.

## Draft

<!-- Links -->

[pulp community health audit]: https://github.com/pulp/pulpproject.org/blob/b037f642cc4d89eb438e32c90b707702e920b977/_posts/2018-09-17-pulp-community-health-audit.md?plain=1#L75
[nextjs governance document]: https://nextjs.org/governance
[gitea]: https://about.gitea.com/
[forjeo]: https://forgejo.org/

<!-- Footnotes -->
[^1]: #
[^2]: https://guidebook.theopensourceway.org/growing-contributors/project-and-community-governance#how-corporate-originated-projects-evolve
