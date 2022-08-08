FROM python:3.8

WORKDIR = .

COPY . .

# Install pip reqs from both user and default
# NOTE: for this implementation, default-reqs.txt specifies
#   the tornado, scikit-learn, and joblib libraries in
#   the format: [library]==[version]. Build the default-reqs.txt
#   file to match your needs
RUN pip install -r requirements.txt

# Expose port 8080
# docker run -p inp_port:internal_port container_image_name 명시 필요
EXPOSE 8080

# The command to start the system
ENTRYPOINT ["python3", "server.py"]