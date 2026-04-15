import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from engine import BinanceEngine
from executor import OrderExecutor
import validators

def main():
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Prime Trade Terminal[/bold cyan]", border_style="cyan"))
    
    if not api_key or not api_secret:
        console.print("[bold red]Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env[/bold red]")
        sys.exit(1)
        
    engine = BinanceEngine(api_key, api_secret)
    executor = OrderExecutor(engine)
    
    while True:
        symbol = Prompt.ask("[cyan]Enter Symbol[/cyan] (e.g., BTCUSDT)").strip().upper()
        if validators.validate_symbol(symbol):
            break
        console.print("[red]Invalid symbol format. Try again.[/red]")
        
    while True:
        side = Prompt.ask("[cyan]Enter Side[/cyan] [green](BUY)[/green] / [red](SELL)[/red]").strip().upper()
        if validators.validate_side(side):
            break
        console.print("[red]Side must be BUY or SELL.[/red]")
        
    while True:
        order_type = Prompt.ask("[cyan]Enter Order Type[/cyan] (MARKET / LIMIT)").strip().upper()
        if validators.validate_order_type(order_type):
            break
        console.print("[red]Order Type must be MARKET or LIMIT.[/red]")
        
    while True:
        qty_str = Prompt.ask(f"[cyan]Enter Quantity for {symbol}[/cyan]").strip()
        is_valid, quantity = validators.validate_quantity(qty_str)
        if is_valid and quantity is not None:
            break
        console.print("[red]Quantity must be a positive number.[/red]")
        
    price = 0.0
    if order_type == "LIMIT":
        while True:
            price_str = Prompt.ask(f"[cyan]Enter Limit Price for {symbol}[/cyan]").strip()
            is_valid, parsed_price = validators.validate_price(price_str, order_type)
            if is_valid and parsed_price is not None:
                price = parsed_price
                break
            console.print("[red]Price must be a positive number for LIMIT orders.[/red]")
            
    dry_run = Confirm.ask("\n[yellow]Enable Dry-Run Mode? (Simulates response without executing)[/yellow]")
    
    notional = "N/A" if order_type == "MARKET" else f"{quantity * price:.2f} USDT"
    
    summary_table = Table(title="Trade Summary")
    summary_table.add_column("Symbol", style="cyan")
    summary_table.add_column("Side", style="green" if side == "BUY" else "red")
    summary_table.add_column("Type", style="magenta")
    summary_table.add_column("Quantity", justify="right")
    summary_table.add_column("Price", justify="right")
    summary_table.add_column("Notional", justify="right", style="yellow")
    
    summary_table.add_row(symbol, side, order_type, str(quantity), "MARKET" if order_type == "MARKET" else str(price), notional)
    console.print("\n")
    console.print(summary_table)
    console.print("\n")
    
    confirm = Confirm.ask(f"[bold red]Proceed with placing this {side} order?[/bold red]")
    if not confirm:
        console.print("[yellow]Order placed cancelled by user.[/yellow]")
        sys.exit(0)
        
    console.print("\n[cyan]Executing order...[/cyan]")
    
    success, response, message = executor.execute(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        dry_run=dry_run
    )
    
    if success:
        console.print("\n[bold green]Order Placement Successful[/bold green]")
        res_table = Table(show_header=True, header_style="bold green")
        res_table.add_column("Field")
        res_table.add_column("Value")
        
        res_table.add_row("Order ID", str(response.get("orderId", "N/A")))
        res_table.add_row("Status", response.get("status", "N/A"))
        if "executedQty" in response:
            res_table.add_row("Executed Qty", str(response.get("executedQty")))
        if "avgPrice" in response:
            res_table.add_row("Avg Price", str(response.get("avgPrice")))
            
        console.print(res_table)
    else:
        console.print(f"\n[bold red]Order Placement Failed[/bold red]")
        console.print(f"[red]Error: {message}[/red]")

if __name__ == "__main__":
    main()
