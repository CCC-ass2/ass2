import toml

# change the background color of the frontend
def change_toml(change):
    data = toml.load('.streamlit/config.toml')

    if change:
        data['theme']['backgroundColor'] = '#AAD3DF'
        data['theme']['secondaryBackgroundColor'] = '#AAD3DF'
    else:
        data['theme']['backgroundColor'] = '#DAE2EF'
        data['theme']['secondaryBackgroundColor'] = '#8393B4'
    # print(data)
    f = open('.streamlit/config.toml', 'w')
    toml.dump(data, f)
    f.close()
