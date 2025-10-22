import pandas as pd
import json
import os
import sys

def _load_lookup_data(lookup_dir):
    all_lookup_df = []

    for filename in os.listdir(lookup_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(lookup_dir, filename)
            with open(filepath, "r") as f:
                data = json.load(f) 

            df = pd.json_normalize (data.get("data",[]))
            
            df['card_market_value'] = (
                df['tcgplayer.prices.holofoil.market']
                .fillna(df['tcgplayer.prices.normal.market'])
                .fillna(0.0)
            )
            df = df.rename(columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name",
            })  
            required_cols = ["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"]
            if all(col in df.columns for col in required_cols):
                all_lookup_df.append(df[required_cols])
            else:
                print(f"Warning: Missing columns in {filename}", file=sys.stderr)
    if not all_lookup_df:
        return pd.DataFrame(columns=["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"])
    
    lookup_df = pd.concat(all_lookup_df)
    lookup_df = lookup_df.sort_values("card_market_value", ascending=False).drop_duplicates(subset=["card_id"], keep='first')
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first")
    return lookup_df
    
def _load_inventory_data(inventory_dir):
    inventory_data = []

    for file in os.listdir(inventory_dir):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(inventory_dir,file))
            if "set_id" in df.columns and "card_number" in df.columns:
                df['card_id'] = df["set_id"].astype(str) + "-" + df["card_number"].astype(str)
            inventory_data.append(df)

    if not inventory_data:
        return pd.DataFrame(columns=["card_id", "card_name", "set_id", "card_number", "binder_name", "page_number", "slot_number"])
            
    inventory_df = pd.concat(inventory_data)
    if "card_id" not in inventory_df.columns:
        inventory_df["card_id"] = inventory_df["set_id"].astype(str)+ "-"+ inventory_df["card_number"].astype(str)
    return inventory_df
    
def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        print("Error, no file found :(", file=sys.stderr)
        pd.DataFrame(columns=[
            "index", "card_id", "card_name", "set_name", "card_market_value",
            "binder_name", "page_number", "slot_number"
        ]).to_csv(output_file,index= False)
        return
    final_df = pd.merge(inventory_df, lookup_df, on="card_id", how="left", suffixes=("", "_drop"))
    
    final_df["card_market_value"] = final_df["card_market_value"].fillna(0.0)
    final_df["set_name"] = final_df["set_name"].fillna("NOT_FOUND")
    
    final_df["index"] = (
        final_df["binder_name"].astype(str) +"-" +
        final_df["page_number"].astype(str)+ "-" +
        final_df["slot_number"].astype(str)
    )
    final_cols = [
        "index", "card_id", "card_name", "set_name", "card_market_value",
        "binder_name", "page_number", "slot_number"
    ]
    final_df[final_cols].to_csv(output_file, index = False)
    print ("Success!!")

def main():
    update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")

def test():
    update_portfolio("./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv")

if __name__ == "__main__":
    print("Script starting Test Mode!", file=sys.stderr)
    test()