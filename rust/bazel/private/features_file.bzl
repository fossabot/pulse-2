"""
Rule that creates a file with the appropriate feature flags given bazel config setting flags
"""

load("@bazel_skylib//rules:common_settings.bzl", "BuildSettingInfo")

def _crate_features_file_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name + ".txt")

    cfg_lines = [
        "--cfg\nfeature=\"%s\"" % flag.label.name
        for flag in ctx.attr.flags
        if flag[BuildSettingInfo].value
    ]
    ctx.actions.write(
        output = out,
        content = "\n".join(cfg_lines),
    )
    return [
        DefaultInfo(files = depset([out])),
    ]

crate_features_file = rule(
    implementation = _crate_features_file_impl,
    attrs = {
        "flags": attr.label_list(),
    },
)
