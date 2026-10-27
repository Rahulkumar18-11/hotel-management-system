from config import Config

class BillingService:
    """Service to handle hotel room, food, tax, and invoice total calculations."""

    @staticmethod
    def calculate_bill(room_price_per_day, number_of_days, food_charges=0.0):
        """
        Calculate complete hotel stay bill using strict 18% GST formula.
        
        Formula:
        - Room Charges = room_price_per_day * number_of_days
        - Subtotal = Room Charges + food_charges
        - GST = Subtotal * GST_RATE (0.18)
        - Total = Subtotal + GST
        """
        try:
            price = float(room_price_per_day)
            days = max(1, int(number_of_days))
            food = float(food_charges) if food_charges else 0.0
        except (ValueError, TypeError):
            price = 0.0
            days = 1
            food = 0.0

        room_charges = round(price * days, 2)
        subtotal = round(room_charges + food, 2)
        gst_rate = Config.GST_RATE  # 0.18
        gst = round(subtotal * gst_rate, 2)
        total_amount = round(subtotal + gst, 2)

        return {
            'room_price_per_day': price,
            'number_of_days': days,
            'room_charges': room_charges,
            'food_charges': food,
            'subtotal': subtotal,
            'gst_rate': gst_rate,
            'gst_percent': int(gst_rate * 100),
            'gst': gst,
            'total_amount': total_amount
        }
