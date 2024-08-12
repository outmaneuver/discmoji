# inkling

## What is inkling?
Inkling is an api wrapper for github, written in python.
Inkling offers you the chance to make a github bot, get a certain user's repositories, and much more.
Inkling is also modern, and a pythonic api at that as well.

## Example

```py
async def main():
    member = await inkling.get_member(name="")
    print(member.repos)

if __name__ == "__main__":
    asyncio.run(main)
```
Of course, this is a very small example, but it gives you a very basic idea of how inkling works.

## Suggestions? 
Open a issue with the label `enhancement`, and follow the template!

## Notes
Inkling needs contributors! contact me (mojidev-py) at pycharmdudeig@gmail.com to become one!