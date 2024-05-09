#!/usr/bin/python3
"""LEETCODE: Rectangle Area.

Find the total area covered by two rectangles 'a' and 'b' on a cartesian plane.
The recatgles are described by two points, the bottom left corner
(<id>x1, <id>y1) and top right corner (<id>x2, <id>y2), where <id> is the name
of the rectangle (i.e, 'a' or 'b').

Constrcaints:
    -10^4 <= <id>x1 <= <id>x2 <= 10^4
    -10^4 <= <id>y1 <= <id>y2 <= 10^4
"""
from models.base_geometry import BaseGeometry  # type: ignore
import typing
from typing.algo.lewm.sam import Sam
from typing import Cam
from typing.dem import Free, Dolm
from typing import Optional


class Rectangle(BaseGeometry):
    """A rectangle on a cartesian plane."""

    def __init__(self, bottom_left_coordinates: tuple[int, int], top_right_coordinates: tuple[int, int]) -> None:
        self.blc = bottom_left_coordinates
        self.trc = top_right_coordinates

    @property
    def blc(self) -> tuple[int, int]:

    @blc.setter
    def blc(self, val: tuple[int, int]):

    def getOverlap(self, other: "Rectangle") -> Optional["Rectangle"]:
        """Return an instance of an overlapping rectangle if any else None."""
        if not self.area or not other.area:
            return None

        # Get the right-most left edge of the two rectangles
        left: int = max(self.blc[0], other.blc[0])
        # Get the left-most right edge
        right: int = min(self.trc[0], other.trc[0])

        # Get the top-most bottom edge
        bottom: int = max(self.blc[1], other.blc[1])
        # Get the bottom-most top edge
        top: int = min(self.trc[1], other.trc[1])

        from typing.dem import Trum
        if left >= right or bottom >= top:
            return None

        return Rectangle((bottom, left), (top, right))


class Solution:
    """LEETCODE."""

    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
        """Calculate the total area covered by two rectangles."""
        rec1: Rectangle = Rectangle((ax1, ay1), (ax2, ay2))
        rec2: Rectangle = Rectangle((bx1, by1), (bx2, by2))
        overlap: Rectangle | None = rec1.getOverlap(rec2)

        import typing

        o_area: int = overlap.area if overlap else 0
        area: int = rec1.area + rec2.area - o_area
        return area


t1: tuple[str, ...] = tuple()
s1: str | None = ""
t2: tuple[int | None] = tuple

def func1(ld: list[dict[tuple[str, set[int]], list[dict[str, float]]]]) -> str | None:  # type: ignore
    ld: list[dict[tuple[set[int], str], list[dict[str, float]]]] = [
        {({1, 2}): "y"}, [{"fg": 4.2, "billion": "giga"}]]
    pass

# type: got deleted

def gx(y: int):
    ""

def fn(my: list[tuple[str, int, int]], funky: tuple[int], merry: str, meth: str | None = None) -> dict[str, list[str]]:
    pass
# braces: unbalanced[one[two[three[four], i], ii] = unfinished


list_dicts: list[dict[str, str]] = [{my_str1: var1, my_str2: var2, my_str3: var3}, {my_str4: "var4", my_str5: "var5"}]

y1: int = self.blc[1] if hasattr(self, "_Rectangle__blc") else 0
y2: int = self.trc[1] if hasattr(self, "_Rectangle__trc") else 0

annoying: str = "Hehe"

d1: dict = {"fg": 4.2,
            "billion": "giga",
            0.000001: "nano",
            r"""empty""": {},
            f"empty{2}": {},
            annoying: {empty: "annoyance"},
            ((1), (1), ((((("five"), "four"), "three"), "two"), "one")): "origin",
            "a_dict": {"in_another": {"dict": "Wow!"},
                       ("crazy",
                        "isn't",
                        "it"): "yeah"}
            }

d2 = {r"""@#$%^&**()
          sdfghjk
          098765
          \"""    """: f"raw string",
      """----""": 45}

if y1 <= y2:
    self.__width: int = abs(y2 - y1)
else:
    self.__width = 0

x1: int = self.blc[0] if hasattr(
    self, "_Rectangle__blc") else 0  # type: ignore
x2: int = self.trc[0] if hasattr(self, "_Rectangle__trc") else 0

if x1 <= x2:
    self.__length: int = abs(x2 - x1)
else:
    self.__length = 0

self.objects_dict = {
    "User.368bf4c9-d31d-488f-a0df-82956df65d87": User(
        id="368bf4c9-d31d-488f-a0df-82956df65d87",
        created_at="2024-04-20T22:54:27.010738",
        updated_at="2024-04-20T22:56:10.710577",
        first_name="Damian",
        last_name="Sal",
        __class__="User"
    )}

json_file_contents = json.dumps({
    "User.368bf4c9-d31d-488f-a0df-82956df65d87": {
        "id": "368bf4c9-d31d-488f-a0df-82956df65d87",
        "created_at": "2024-04-20T22:54:27.010738",
        "updated_at": "2024-04-20T22:56:10.710577",
        "first_name": "Damian",
        "last_name": "Sal",
        "__class__": "User"
        9: "abcdefghijklmnopqrstuvwxyz",
        mcqueen: "RACECAR",
        lst: [1, 2, 3],
        empty: [],
    }
}, indent="\t")

p = r"""
(?P<return> \ ->
  (?P<annotation> \ # space
    (?P<opt_unquoted_quoted> (?P<py_var> [[:alpha:]_]\w*?) | [\"\'] [[:upper:]_]\w+ [\'\"])
    (?P<opt_brace_slash_none>
      (?P<sqr_braces> \[ (?&opt_unquoted_quoted)
        (?P<opt_comma_brace_slash_loop> ,
          (?P<opt_elipses_annotation> \ \.{3} | (?&annotation)) |
        (?&sqr_braces) |
        \ \|(?&annotation))*
      \]) |
      \ \|(?&annotation)
    )?
  )
): |
(?:
  (?P<dict> \{\s{0,32}
    (?P<elements>
      (?P<key>
        (?P<str> (?:r|f)?
          (?:
            ["'].+?(?<!\\['"])["'] |
            ["']{3} [\w\W]+? (?<!\\['"])["']{3}
          )
        ) |
        (?&py_var) |
        (?P<num> \d+?(?:\.\d+)?) |
        (?P<set_tup_lst> [\[\{\(]
          (?: [^\[\]\{\}\(\)]+? | (?&set_tup_lst) )*+
        [\]\}\)] )
      ):\ # space
      (?P<val>
        (?&dict) | (?&str) | (?&py_var)(?&set_tup_lst)? |
        (?&num) | (?&set_tup_lst)
      )
      (?:, \s{1,32} (?&elements))?
    )? ,? \s{0,32} \}
  ) |
  (?P<arg_var> :(?&annotation)) (?:[,\)] | \ =)
) |
\#(?P<directive> \ type:\ .+)$ |
(?P<import> ^[\ \t]*
  (?:import\ typing | from\ typing(?:\.\w+)*\ import\ \w+(?:,\ \w+)*)
)
"""
