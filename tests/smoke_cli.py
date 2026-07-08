import subprocess
import sys
import tempfile
import shutil
import os

# This script copies the project to a temp directory and runs main.py
# with a scripted interactive session to exercise core CLI flows.

PROJECT_FILES = [
    'auth.py', 'books.py', 'members.py', 'borrow.py', 'file_handler.py', 'utils.py', 'main.py',
    'books.json', 'members.json', 'users.json', 'borrow_records.json', 'README.md'
]

inputs = [
    # Register Admin
    '1',  # Register
    'AdminSmoke',
    'adminpass',
    '1',  # role Admin
    # Login as Admin
    '2',
    'AdminSmoke',
    'adminpass',
    # Admin Dashboard -> Book Management
    '1',
    '1',  # Add Book
    'B100',
    'Smoke Book',
    'Smoke Author',
    'Fiction',
    '1',  # quantity
    '6',  # Back
    # Member Management -> Register Member
    '2',
    '1',
    'M200',
    'Smoke Member',
    'smoke@member.test',
    '1234567890',
    '6',  # Back
    # Borrow & Return -> Issue Book
    '3',
    '1',
    'M200',
    'B100',
    '3',  # View Borrow Records
    '5',  # Back
    # Logout
    '4',
    # Exit
    '3'
]

def run_smoke():
    tmp = tempfile.mkdtemp(prefix='lms_smoke_')

    try:
        # copy files
        for f in PROJECT_FILES:
            if os.path.exists(f):
                shutil.copy(f, tmp)

        # ensure JSON files exist
        for jf in ['books.json', 'members.json', 'users.json', 'borrow_records.json']:
            path = os.path.join(tmp, jf)
            if not os.path.exists(path):
                with open(path, 'w') as fh:
                    fh.write('[]')

        cmd = [sys.executable, 'main.py']

        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        proc = subprocess.run(
            cmd,
            cwd=tmp,
            input='\n'.join(inputs) + '\n',
            capture_output=True,
            timeout=15,
            text=True,
            env=env
        )

        out = proc.stdout + proc.stderr

        checks = [
            'Registration Successful',
            'Login Successful',
            'Book Added Successfully',
            'Member Registered Successfully',
            'Book Issued Successfully'
        ]

        passed = True
        missing = []

        for c in checks:
            if c not in out:
                passed = False
                missing.append(c)

        print('--- SMOKE OUTPUT ---')
        print(out)
        print('--- END OUTPUT ---')

        if passed:
            print('SMOKE TEST: PASS')
            return 0
        else:
            print('SMOKE TEST: FAIL - missing:', missing)
            return 2

    except subprocess.TimeoutExpired:
        print('SMOKE TEST: TIMEOUT')
        return 3

    finally:
        shutil.rmtree(tmp)

if __name__ == '__main__':
    rc = run_smoke()
    sys.exit(rc)
