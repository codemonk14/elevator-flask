from flask import Flask, request, render_template, redirect, url_for
from models import db, Elevator, UserRequest,log_movement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator_system.db'

db.init_app(app)

def initialize_elevators():
    if Elevator.query.count() == 0:
        elevators = [
            Elevator(elevator_id='A'),
            Elevator(elevator_id='B'),
            Elevator(elevator_id='C'),
            Elevator(elevator_id='D')
        ]
        db.session.bulk_save_objects(elevators)
        db.session.commit()

# Initialize database and populate with initial data
with app.app_context():
    db.create_all()
    initialize_elevators()

@app.route('/')
def index():
    elevators = Elevator.query.all()
    return render_template('index.html', elevators=elevators)

@app.route('/request', methods=['POST'])
def request_elevator():
    current_floor = int(request.form['current_floor'])
    destination_floor = int(request.form['destination_floor'])
    num_people = int(request.form['num_people'])

    # Find the nearest available elevator
    elevators = Elevator.query.all()
    if not elevators:
        return "No elevators available", 400

    nearest_elevator = min(
        elevators, 
        key=lambda e: (abs(e.current_floor - current_floor), e.people_count)
    )

    if nearest_elevator.people_count + num_people <= 20:        
        nearest_elevator.people_count += num_people
        nearest_elevator.current_floor = current_floor
        nearest_elevator.direction = '^' if destination_floor > current_floor else 'V'
        db.session.commit()

        user_request = UserRequest(
            current_floor=current_floor,
            destination_floor=destination_floor,
            elevator_id=nearest_elevator.elevator_id,
            people_count=num_people
        )
        db.session.add(user_request)
        db.session.commit()
    else:
        return "Elevator is full", 400

    return redirect(url_for('index'))

@app.route('/process')
def process_requests():
    requests = UserRequest.query.all()
    for req in requests:
        elevator = Elevator.query.filter_by(elevator_id=req.elevator_id).first()
        elevator.current_floor = req.destination_floor
        elevator.people_count = max(0, elevator.people_count - req.people_count)
        elevator.direction = '-'
        db.session.delete(req)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/status')
def status():
    elevators = Elevator.query.all()
    return render_template('status.html', elevators=elevators)

@app.route('/users_status')
def user_status():
    users = UserRequest.query.all()
    return render_template('user_status.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)