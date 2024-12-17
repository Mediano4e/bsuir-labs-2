from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import psycopg2
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="postgres", 
        host="postgres", 
        port="5432"
    )
    return conn

class Organization(BaseModel):
    code: str
    full_name: str
    short_name: str
    address: str
    specialization: str
    bank_details: str

@app.get("/")
async def main_menu(request: Request):
    return templates.TemplateResponse("main_menu.html", {"request": request, "message": None})

@app.get("/add_organization_form")
async def add_organization_form(request: Request):
    return templates.TemplateResponse("add_organization_form.html", {"request": request})

@app.post("/add_organization")
async def add_organization(
    request: Request,
    code: str = Form(...),
    full_name: str = Form(...),
    short_name: str = Form(...),
    address: str = Form(...),
    specialization: str = Form(...),
    bank_details: str = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("%s, %s, %s, %s, %s, %s", code, full_name, short_name, address, specialization, bank_details)
        cur.execute(
            "CALL add_organization(%s, %s, %s, %s, %s, %s);",
            (code, full_name, short_name, address, specialization, bank_details)
        )
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Organization added successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})

@app.get("/update_organization_form")
async def update_organization_form(request: Request):
    return templates.TemplateResponse("update_organization_form.html", {"request": request})


@app.post("/update_organization")
async def update_organization(
    request: Request,
    org_id: int = Form(...),
    code: str = Form(...),
    full_name: str = Form(...),
    short_name: str = Form(...),
    address: str = Form(...),
    specialization: str = Form(...),
    bank_details: str = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Updating ID: %s with data: %s, %s, %s, %s, %s, %s", id, code, full_name, short_name, address, specialization, bank_details)
        cur.execute(
            "CALL update_organization(%s, %s, %s, %s, %s, %s, %s);",
            (org_id, code, full_name, short_name, address, specialization, bank_details)
        )
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Organization updated successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/delete_organization_form")
async def delete_organization_form(request: Request):
    return templates.TemplateResponse("delete_organization_form.html", {"request": request})


@app.post("/delete_organization")
async def delete_organization(request: Request, org_id: int = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Deleting organization with ID: %s", org_id)
        cur.execute("CALL delete_organization(%s);", (org_id,))
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Organization deleted successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/add_employee_form")
async def add_employee_form(request: Request):
    return templates.TemplateResponse("add_employee_form.html", {"request": request})


@app.post("/add_employee")
async def add_employee(
    request: Request,
    full_name: str = Form(...),
    age: int = Form(...),
    risk_category: int = Form(...),
    contract_id: int = Form(...),
    organization_id: int = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Adding employee: %s, %s, %s, %s, %s", full_name, age, risk_category, contract_id, organization_id)
        cur.execute(
            "CALL add_employee(%s, %s, %s, %s, %s);",
            (full_name, age, risk_category, contract_id, organization_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Employee added successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/update_employee_form")
async def update_employee_form(request: Request):
    return templates.TemplateResponse("update_employee_form.html", {"request": request})


@app.post("/update_employee")
async def update_employee(
    request: Request,
    emp_id: int = Form(...),
    full_name: str = Form(...),
    age: int = Form(...),
    risk_category: int = Form(...),
    contract_id: int = Form(...),
    organization_id: int = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Updating employee ID: %s with data: %s, %s, %s, %s, %s", emp_id, full_name, age, risk_category, contract_id, organization_id)
        cur.execute(
            "CALL update_employee(%s, %s, %s, %s, %s, %s);",
            (emp_id, full_name, age, risk_category, contract_id, organization_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Employee updated successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/delete_employee_form")
async def delete_employee_form(request: Request):
    return templates.TemplateResponse("delete_employee_form.html", {"request": request})


@app.post("/delete_employee")
async def delete_employee(request: Request, emp_id: int = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Deleting employee with ID: %s", emp_id)
        cur.execute("CALL delete_employee(%s);", (emp_id,))
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Employee deleted successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/add_agent_form")
async def add_agent_form(request: Request):
    return templates.TemplateResponse("add_agent_form.html", {"request": request})


@app.post("/add_agent")
async def add_agent(
    request: Request,
    full_name: str = Form(...),
    passport_data: str = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Adding agent: %s, %s", full_name, passport_data)
        cur.execute(
            "CALL add_agent(%s, %s);", (full_name, passport_data)
        )
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Agent added successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/update_agent_form")
async def update_agent_form(request: Request):
    return templates.TemplateResponse("update_agent_form.html", {"request": request})


@app.post("/update_agent")
async def update_agent(
    request: Request,
    agent_id: int = Form(...),
    full_name: str = Form(...),
    passport_data: str = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Updating agent ID: %s with data: %s, %s", agent_id, full_name, passport_data)
        cur.execute(
            "CALL update_agent(%s, %s, %s);", (agent_id, full_name, passport_data)
        )
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Agent updated successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/delete_agent_form")
async def delete_agent_form(request: Request):
    return templates.TemplateResponse("delete_agent_form.html", {"request": request})


@app.post("/delete_agent")
async def delete_agent(request: Request, agent_id: int = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Deleting agent with ID: %s", agent_id)
        cur.execute("CALL delete_agent(%s);", (agent_id,))
        conn.commit()
        cur.close()
        conn.close()
        success_message = "Agent deleted successfully"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": success_message, "message_type": "success"})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return templates.TemplateResponse("main_menu.html", {"request": request, "message": error_message, "message_type": "error"})


@app.get("/get_active_contracts_by_date_form")
async def get_active_contracts_by_date_form(request: Request):
    return templates.TemplateResponse("get_active_contracts_by_date.html", {"request": request})


@app.post("/get_active_contracts_by_date")
async def get_active_contracts_by_date(
    request: Request,
    org_id: int = Form(...),
    p_date: str = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_active_contracts_by_date(%s, %s);", (org_id, p_date))
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]  # Получение имён столбцов
        cur.close()
        conn.close()
        
        return templates.TemplateResponse(
            "results_table.html",
            {
                "request": request,
                "message": "Query executed successfully!",
                "message_type": "success",
                "columns": columns,
                "rows": results
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "results_table.html",
            {
                "request": request,
                "message": f"Error: {str(e)}",
                "message_type": "error",
                "columns": [],
                "rows": []
            }
        )



@app.get("/get_active_agents_by_date_form")
async def get_active_contracts_by_date_form(request: Request):
    return templates.TemplateResponse("get_active_agents_by_date.html", {"request": request})


@app.post("/get_active_agents_by_date")
async def get_active_agents_by_date(
    request: Request,
    org_id: int = Form(...),
    p_date: str = Form(...)
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_agents_for_organization_on_date(%s, %s);", (org_id, p_date))
        
        results = cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        
        cur.close()
        conn.close()

        return templates.TemplateResponse(
            "results_table.html",
            {
                "request": request,
                "message": "Query executed successfully!",
                "message_type": "success",
                "columns": columns,
                "rows": results
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "results_table.html",
            {
                "request": request,
                "message": f"Error: {str(e)}",
                "message_type": "error",
                "columns": [],
                "rows": []
            }
        )


@app.get("/get_insurance_payments_form")
async def get_insurance_payments_form(request: Request):
    return templates.TemplateResponse("get_insurance_payments_form.html", {"request": request})


@app.post("/get_insurance_payments")
async def get_insurance_payments(
    request: Request,
    p_date: str = Form(...),
):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_insurance_payments(%s);", (p_date,))
        
        results = cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        
        cur.close()
        conn.close()

        return templates.TemplateResponse(
            "results_table.html",
            {
                "request": request,
                "message": "Query executed successfully!",
                "message_type": "success",
                "columns": columns,
                "rows": results
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "results_table.html",
            {
                "request": request,
                "message": f"Error: {str(e)}",
                "message_type": "error",
                "columns": [],
                "rows": []
            }
        )
