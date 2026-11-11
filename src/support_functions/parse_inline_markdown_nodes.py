import re


def parse_inline_nodes(markdown):
    if markdown == "":
        return []

    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)|\[([^\[\]]+)\]\(([^\(\)]*)\)"
    matches = re.finditer(pattern, markdown)

    nodes = []
    current_index = 0

    for match in matches:
        start = match.start()
        end = match.end()

        if start > current_index:
            text_part = markdown[current_index:start]
            nodes.append(("text", text_part))

        image_alt = match.group(1)
        image_url = match.group(2)
        link_label = match.group(3)
        link_url = match.group(4)

        if image_alt is not None:
            nodes.append(("image", image_alt, image_url))
        else:
            nodes.append(("link", link_label, link_url))

        current_index = end

    if current_index < len(markdown):
        nodes.append(("text", markdown[current_index:]))

    if len(nodes) == 0:
        nodes.append(("text", markdown))

    return nodes


run_cases = [
    (
        "Read [Boot.dev](https://boot.dev) and see ![logo](/logo.png)",
        [
            ("text", "Read "),
            ("link", "Boot.dev", "https://boot.dev"),
            ("text", " and see "),
            ("image", "logo", "/logo.png"),
        ],
    ),
    (
        "Just plain text",
        [("text", "Just plain text")],
    ),
    (
        "Use [docs](/docs) or [guide](/guide) today",
        [
            ("text", "Use "),
            ("link", "docs", "/docs"),
            ("text", " or "),
            ("link", "guide", "/guide"),
            ("text", " today"),
        ],
    ),
]

submit_cases = run_cases + [
    (
        "![hero](/hero.png) starts here",
        [
            ("image", "hero", "/hero.png"),
            ("text", " starts here"),
        ],
    ),
    (
        "![a](/a.png)[b](/b)",
        [
            ("image", "a", "/a.png"),
            ("link", "b", "/b"),
        ],
    ),
    (
        "Open ![icon](/icon.svg) then visit [profile](/u/me) now",
        [
            ("text", "Open "),
            ("image", "icon", "/icon.svg"),
            ("text", " then visit "),
            ("link", "profile", "/u/me"),
            ("text", " now"),
        ],
    ),
]


def test(markdown, expected_output):
    print("---------------------------------")
    print(f"Input: {markdown}")
    print("")
    result = parse_inline_nodes(markdown)
    print(f"Expected: {expected_output}")
    print(f"Actual:   {result}")
    if result == expected_output:
        return True
    return False


def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
            print("Pass")
        else:
            failed += 1
            print("Fail")
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()
