 ---

## 🚀 Migration: Move Domain Objects from TypeScript to Python  

### 📄 **Related Issue**  
Closes #1  

### ✅ **Description**  
This PR migrates domain objects from TypeScript to Python. The following changes have been made:  
- Converted TypeScript domain entities to Python using **Pydantic models**.  
- Moved **enums** to Python's enum.Enum structure.  
- Implemented abstract base classes where applicable.  
- Ensured Pythonic naming conventions (camelCase → snake_case).  
- Refactored repository patterns for Python-based storage.  

### 🔄 **Changes Made**  

- **Repositories:**  
  - [x] Migrated `base_in_memory_repository.ts` → `base_in_memory_repository.py`  
  - [x] Added `borrower_repository.py`  
  - [x] Added `library_repository.py`  
  - [x] Added `loan_repository.py`  
  - [x] Added `person_repository.py`  
  - [x] Added `test_library_repository.py`  
  - [x] Added `test_loan_repository.py`  

- **Entities:**  
  - [x] Added `people/user.py`  

- **Value Objects:**  
  - [x] Updated `value_items/exceptions.py`  
  - [x] Updated `value_items/location/__init__.py`  
  - [x] Added `value_items/user_roles.py`  

### 🔍 **How to Test**  
1. Ensure all migrated files exist in the repository.  
2. Run `pytest` or `pdm run test` to verify functionality.  
3. Check for PEP8 compliance using `flake8` or `black`.  
4. Validate repository logic with integration tests.  

### 🛠️ **Screenshots / GIFs (if applicable)**  
_(Optional, add images showing any UI or code changes)_  

### ⚠️ **Checklist before merge**  
- [ ] Code follows project conventions  
- [ ] All unit tests pass  
- [ ] No breaking changes introduced  
- [ ] PR reviewed and approved  

---

👥 **Reviewers:**  
Tag relevant reviewers: @mathiesonsterling 

---

