# This code is licensed under the MIT License.
# Copyright (c) [2025-01-28] [Akihito Miyazaki]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Note that the GraphQL query texts included in this file are for illustrative purposes
# and are quoted from the Linear API documentation. They are not covered by the MIT License.
# See: https://developers.linear.app/docs/graphql/working-with-the-graphql-api


import codecs
import json
import os


from linear_api_utils import load_api_key, execute_query

"""
このスクリプトでは、以下のページに含まれるQueryを実行します。
https://developers.linear.app/docs/graphql/working-with-the-graphql-api/filtering

　Filteringは開発状況がAlphaで後で変更になる可能性もあります。（動かないことがあります。そういう現象が確認できたらissueにあげてください)

　お使いのLinearの状態によって返ってくる値は異なります。値が空なことも有りえます。
Issueの数が多かったり、頻繁に呼び出すと、Rate-Limitの関係でエラーになることがあります。

　注意事項
絵文字はWindowsのPowerShellとかで、化ける可能性があります。
出力をコピーペストするとVSCode等では正常に表示されます。

なお最後のExampleは動かなかったので、大幅に変更しています。




"""

if __name__ == "__main__":
    api_key = load_api_key()

    high_priority_issues_text = """
query HighPriorityIssues {
  issues(filter: { 
    priority: { lte: 2 }
  }) {
    nodes {
      id, title, priority
    }
  }
}
"""
    result = execute_query("HighPriorityIssues", high_priority_issues_text, api_key)

    high_priority_issues_text = """
query HighPriorityIssues {
  issues(filter: { 
    priority: { lte: 2, neq: 0 }
  }) {
    nodes {
      id, title, priority
    }
  }
}
"""
    result = execute_query("HighPriorityIssues2", high_priority_issues_text, api_key)

    null_description_text = """
query Issues {
  issues(filter: { 
    description: { null: true }
  }) {
    nodes {
      id, title, description
    }
  }
}
"""
    result = execute_query("HighPriorityIssues2", high_priority_issues_text, api_key)

    logical_operations_txt = """
query Issues {
  issues(filter: { 
    priority: { eq: 1 }
    dueDate: { lte: "2021" }
  }) {
    nodes {
      id, title, priority, dueDate
    }
  }
}
"""
    result = execute_query("logical operations", logical_operations_txt, api_key)

    logical_operations_or_txt = """
query Issues {
  issues(filter: { 
    or: [
      { priority: { eq: 4 } },
      { priority: { eq: 0 } }
    ]
    dueDate: { lte: "2021" }
  }) {
    nodes {
      id, title, priority, dueDate
    }
  }
}
    """
    result = execute_query("logical operations or", logical_operations_or_txt, api_key)

    assigned_issues_txt = """
query AssignedIssues {
  issues(filter: { 
    assignee: { email: { eq: "john@linear.app" } }
  }) {
    nodes {
      id
      title
      assignee {
        name
      }
    }
  }
}
    """
    result = execute_query("AssignedIssues", assigned_issues_txt, api_key)

    issues_bug_txt = """
query Issues {
  issues(filter: { 
    labels: { name: { eq: "Bug" } }
  }) {
    nodes {
      id, title
    }
  }
}
    """
    result = execute_query("Issues Bug", issues_bug_txt, api_key)

    issues_bug_every_txt = """
query Issues {
  issues(filter: { 
    labels: { every: { name: { eq: "Bug" } } }
  }) {
    nodes {
      id, title
    }
  }
}
    """
    result = execute_query("Issues Bug every", issues_bug_every_txt, api_key)

    issues_due_txt = """
query IssuesDue {
  issues(filter: { 
    dueDate: { lt: "P2W" }
  }) {
    nodes {
      id, title
    }
  }
}
    """
    result = execute_query("Issues Due", issues_due_txt, api_key)

    example_projects_txt = """
query Projects {
  projects(filter: { 
    lead: { name: { startsWith: "John" } } 
  }) {
    nodes {
      issues(filter: { 
        labels: { name: { in: ["Bug", "Defect"] } } 
      }) {
        nodes {
          id
          title
        }
      }
    }
  }
}
    """
    result = execute_query(
        "Example Projects(WindowsのPowerShellだと表示は化けますが正常です)",
        example_projects_txt,
        api_key,
    )
    # assignedIssuesなので注意（一人で使っていると普通asignしない)

    example_thumbup_txt = """
query Issues {
  viewer {
    assignedIssues(filter: { 
      comments: { body: { contains: "👍" } } 
    }) {
      nodes {
        id
        title
      }
    }
  }
}
    """
    result = execute_query("Example Thumbup", example_thumbup_txt, api_key)

    closed_issues_txt = """
query ClosedIssues {
  viewer {
    createdIssues(filter: { completedAt: { gt: "-P2W" } }) {
      nodes {
        id, title
      }
    }
  }
}
    """
    result = execute_query("ClosedIssues", closed_issues_txt, api_key)

    # おそらく、estimate: { eq: 0 }　は効果ない。estimate: { null: true }
    # StateやStatusには、名前とtypeがあります。設定で変更可能です。
    # ProjectのStateは、DEPRECATEDです。
    started_no_estimate_issues_txt = """
query Issues {
  issues(
    filter: {
      estimate: { null: true }
      state:{type:{ eq: "started" }}
      project:{status:{type:{ eq: "started" }}}
    }
  ) {
    nodes {
      title
      estimate
      state{
      name
      type
      }
      project {
        name
        status{
        name
        type
        }
      }
    }
  }
}
    """
    result = execute_query(
        "Started No Estimate", started_no_estimate_issues_txt, api_key
    )
