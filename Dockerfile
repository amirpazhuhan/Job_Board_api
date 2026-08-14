# Pull base image
FROM python:3.14.6-trixie
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Copy project
COPY . .

CMD ["gunicorn", "mini_ecommerce.wsgi:application", "--bind", "0.0.0.0:10000"]