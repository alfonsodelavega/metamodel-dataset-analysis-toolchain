#!/usr/bin/env python

#%%
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import re
import collections
import os
import shutil

#%%

filename = "AMMORE2020-Dataset - ValidationErrors.csv"

df = pd.read_csv(filename)
df.columns

#%%
metamodels_with_errors = df.artifact.unique()
print(len(metamodels_with_errors))

#%%
proxy_error_code = 4

metamodels_with_proxy_errors_only = []
for metamodel in metamodels_with_errors:
    df_mm = df[df.artifact == metamodel]
    if len(df_mm.errorcode.unique()) == 1 and df_mm.iloc[0].errorcode == proxy_error_code:
        metamodels_with_proxy_errors_only.append(metamodel)

print(metamodels_with_proxy_errors_only)

#%%
df_proxies = df[df.artifact.isin(metamodels_with_proxy_errors_only)]

assert(len(df_proxies.artifact.unique()) == len(metamodels_with_proxy_errors_only))
assert(len(df_proxies.errorcode.unique()) == 1 and df_proxies.iloc[0].errorcode == proxy_error_code)

#%%
proxy_errors = df_proxies.message.unique()

#%%
regexp = re.compile("^The feature .* contains an unresolved proxy 'org.eclipse.emf.ecore.impl.*{(.*)#.*'")

errors = []
counter = 0
for error in proxy_errors:
    result = regexp.search(error)
    if (result):
        counter += 1
        errors.append(result.group(1))
        # print(result.group(1))
    # else:
    #     print(error)

print(counter)
print(len(proxy_errors))

#%%
proxy_counter = collections.Counter(errors)
proxies = proxy_counter.keys()
print("Unique errors:", len(proxies))

uri_types = collections.Counter([proxy.split(":")[0] for proxy in proxies])
print(uri_types)

#%%
for key, value in proxy_counter.most_common():
    if (value > 50):
        print(key, ":", value)

#%%
http_uris = [uri for uri in proxies if uri.startswith("http")]
for uri in http_uris:
    print(uri)

#%%
with open("metamodels_with_errors.txt", "w") as output_file:
    for metamodel_file in df.artifact.unique():
        print(metamodel_file, file=output_file)

# to fix the maximum number of metamodels, get the unique proxies at metamodel level first (so that a model with 500 errors does not bias the results)

# test first how to use the "metamodels-with-errors.txt" file from within java

# check file duplicates from terminal


#%%
all_metamodels = os.listdir("../metamodels")

#%%
metamodels_without_errors = set(all_metamodels) - set(metamodels_with_errors)

with open("metamodels_without_errors.txt", "w") as output_file:
    for mm in metamodels_without_errors:
        print(mm, file=output_file)

#%%
metamodels_without_errors_folder = "../metamodels-no-errors"
if not os.path.exists(metamodels_without_errors_folder):
    os.makedirs(metamodels_without_errors_folder)

for mm in metamodels_without_errors:
    shutil.copy("{}/{}".format("../metamodels", mm),
                "{}/{}".format(metamodels_without_errors_folder, mm))
