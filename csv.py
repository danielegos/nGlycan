import pandas as pd

# Example DataFrames with repeated column names
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})

# Concatenate DataFrames, resulting in repeated column names
df_concat = pd.concat([df1, df2])
print("Concatenated DataFrame with repeated columns:\n", df_concat)

# Rename columns before concatenation
df1_renamed = df1.rename(columns={'A': 'A_df1'})
df2_renamed = df2.rename(columns={'A': 'A_df2'})
df_concat_renamed = pd.concat([df1_renamed, df2_renamed])
print("\nConcatenated DataFrame with renamed columns:\n", df_concat_renamed)

# Concatenate with MultiIndex for columns
df_concat_multiindex = pd.concat([df1, df2], keys=['df1', 'df2'])
print("\nConcatenated DataFrame with MultiIndex columns:\n", df_concat_multiindex)

# Drop duplicate columns after concatenation
df_concat_dropped = df_concat.loc[:, ~df_concat.columns.duplicated()]
print("\nConcatenated DataFrame with duplicate columns dropped:\n", df_concat_dropped)