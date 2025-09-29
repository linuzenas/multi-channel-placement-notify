import os
import sys
from app import app, db, User

def fix_placement_status():
    """Fix placement status to be consistent"""
    
    with app.app_context():
        # Update any students with inconsistent placement status
        students = User.query.filter_by(role='student').all()
        
        for student in students:
            if student.placement_status and student.placement_status.lower() == 'unplaced':
                student.placement_status = 'Not Placed'
                print(f"Updated {student.name} placement status to 'Not Placed'")
        
        db.session.commit()
        print("Placement status fix completed!")

if __name__ == '__main__':
    fix_placement_status()